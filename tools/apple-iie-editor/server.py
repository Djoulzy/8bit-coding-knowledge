#!/usr/bin/env python3
"""Local editor service with optional adapter-controlled project saving."""
import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit, unquote

HERE = Path(__file__).resolve().parent
from project_format import validate_project


def load_adapter(name):
    if not name:
        return None
    import importlib.util
    path = (HERE.parents[1] / 'ports/laigle-dor/apple-iie/tools/editor_adapter.py'
            if name == 'laigle-dor' else Path(name).expanduser().resolve())
    spec = importlib.util.spec_from_file_location('a2_optional_adapter', path)
    if spec is None or spec.loader is None:
        raise ValueError('Invalid adapter module')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not callable(getattr(module, 'assets', None)):
        raise ValueError('Adapter must expose assets()')
    return module


class Handler(BaseHTTPRequestHandler):
    def local_host(self):
        return self.headers.get('Host') in ('127.0.0.1:%d' % self.server.server_port,
                                            'localhost:%d' % self.server.server_port)

    def library(self):
        return self.server.adapter.assets() if self.server.adapter else {}

    def respond(self, status, body, mime='application/json; charset=utf-8'):
        self.send_response(status)
        self.send_header('Content-Type', mime)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Content-Security-Policy', "default-src 'self'; img-src 'self' blob: data:; style-src 'self' 'unsafe-inline'; connect-src 'self'; frame-ancestors 'none'")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        # Paths stay fixed: adapters own any project-file access.
        if not self.local_host():
            self.respond(403, b'{"error":"Local host required"}')
            return
        path = unquote(urlsplit(self.path).path)
        try:
            if path == '/api/config':
                info = getattr(self.server.adapter, 'project_info', None)
                self.respond(200, json.dumps({'library': getattr(self.server.adapter, 'TITLE', None),
                    'project': info() if callable(info) and callable(getattr(self.server.adapter, 'save_project', None)) else None}).encode())
            elif path == '/api/project':
                load = getattr(self.server.adapter, 'load_project', None)
                if not callable(load):
                    self.respond(404, b'{"error":"No local project adapter"}')
                else:
                    self.respond(200, json.dumps(validate_project(load())).encode())
            elif path == '/api/catalog':
                items = [{k: a[k] for k in ('key', 'name', 'kind', 'mode')} for a in self.library().values()]
                self.respond(200, json.dumps(items).encode())
            elif path.startswith('/api/asset/'):
                a = self.library().get(path[len('/api/asset/'):])
                if a is None:
                    self.respond(404, b'{"error":"Unknown asset"}')
                else:
                    self.respond(200, json.dumps(a).encode())
            else:
                files = {'/': ('index.html', 'text/html; charset=utf-8'),
                         '/app.js': ('app.js', 'text/javascript; charset=utf-8'),
                         '/core.js': ('core.js', 'text/javascript; charset=utf-8'),
                         '/workspace.js': ('workspace.js', 'text/javascript; charset=utf-8'),
                         '/workspace-tests.js': ('tests/workspace-tests.js', 'text/javascript; charset=utf-8'),
                         '/style.css': ('style.css', 'text/css; charset=utf-8'),
                         '/tests.html': ('tests/tests.html', 'text/html; charset=utf-8'),
                         '/tests.js': ('tests/tests.js', 'text/javascript; charset=utf-8'),
                         '/preview-vectors.json': ('tests/preview-vectors.json', 'application/json')}
                if path not in files:
                    self.respond(404, b'Not found', 'text/plain')
                    return
                filename, mime = files[path]
                self.respond(200, (HERE / filename).read_bytes(), mime)
        except (ValueError, OSError) as exc:
            self.respond(500, json.dumps({'error': str(exc)}).encode())

    def do_POST(self):
        # Browser writes require a same-origin JSON request; no caller-supplied
        # filesystem path and no write capability without an explicit adapter.
        if not self.local_host() or self.headers.get('Origin') != 'http://' + self.headers.get('Host', ''):
            self.respond(403, b'{"error":"Same-origin local request required"}')
            return
        if urlsplit(self.path).path != '/api/project':
            self.respond(404, b'{"error":"Unknown endpoint"}')
            return
        save = getattr(self.server.adapter, 'save_project', None)
        if not callable(save):
            self.respond(405, b'{"error":"No writable project adapter"}')
            return
        if self.headers.get('Content-Type', '').split(';')[0].strip() != 'application/json':
            self.respond(415, b'{"error":"JSON required"}')
            return
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 < length <= 64 * 1024 * 1024:
                self.respond(413, b'{"error":"Project must be between 1 byte and 64 MiB"}')
                return
            workspace = validate_project(json.loads(self.rfile.read(length)))
            if workspace['schema'] != 'a2-workspace-v2':
                raise ValueError('Expected a complete editor workspace')
            self.respond(200, json.dumps(save(workspace)).encode())
        except (ValueError, TypeError, KeyError) as exc:
            self.respond(400, json.dumps({'error': str(exc)}).encode())
        except OSError as exc:
            self.respond(500, json.dumps({'error': 'Enregistrement impossible : ' + str(exc)}).encode())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8770)
    parser.add_argument('--adapter', help='Optional trusted Python library module path, or laigle-dor')
    parser.add_argument('--check', type=Path, help='Validate an exported project, without starting the server')
    args = parser.parse_args()
    if args.check:
        project = validate_project(json.loads(args.check.read_text()))
        if args.adapter and project.get('schema') == 'a2-artwork-v1':
            adapter = load_adapter(args.adapter)
            known = adapter.assets()
            for a in project['assets']:
                prefix = getattr(adapter, 'KEY_PREFIX', None)
                if prefix and a['key'].startswith(prefix) and a['key'] not in known:
                    raise ValueError('Unknown adapter resource: ' + a['key'])
                if a['key'] in known:
                    for field in ('mode', 'kind', 'width', 'height', 'encoding', 'mixed'):
                        if a.get(field) != known[a['key']].get(field):
                            raise ValueError('Adapter asset contract differs: ' + field)
        print('Valid project: ' + project['schema'])
        return
    adapter = load_adapter(args.adapter)
    server = ThreadingHTTPServer(('127.0.0.1', args.port), Handler)
    server.adapter = adapter
    print('Apple IIe Atelier → http://127.0.0.1:%d (Ctrl-C to stop)' % server.server_port, flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
