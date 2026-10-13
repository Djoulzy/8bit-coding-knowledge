"""Run the actual NMOS program in a functional CPU harness, headless or local UI."""
import argparse
import base64
from collections import deque
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.common import ROOT, digest, write_json
from tools.machine import Machine
from tools.preview import png

HTML = '''<!doctype html><html lang="en"><meta charset="utf-8">
<title>L'Aigle d'Or — Apple IIe W06</title><style>
body{background:#10131b;color:#e7e8ef;font:16px system-ui;margin:30px auto;max-width:900px;padding:0 20px}
h1{font-size:26px}img{width:840px;max-width:100%;image-rendering:pixelated;background:black;border:1px solid #606477}
code{color:#fbc878}button{padding:9px 14px;margin:4px;background:#272e41;color:white;border:1px solid #606477;cursor:pointer}
.note{color:#fbc878}pre{font-size:13px;white-space:pre-wrap}</style>
<h1>L'Aigle d'Or · Apple IIe · room 12</h1>
<p class="note">Mixed HGR + text · double buffer · monochrome · provisional room variation</p>
<img id="screen" alt="Executed Apple HGR screen, room 12">
<p>Arrows: turn, then walk. Movement continues after release. Space: stop / stand.
A: crouch. R: restart. Alternate directions: J / K / U / N.</p>
<div><button data-code="8">← Left</button><button data-code="21">Right →</button>
<button data-code="11">↑ Up</button><button data-code="10">↓ Down</button>
<button data-code="65">A · Crouch</button><button data-code="32">Space · Stop</button>
<button data-code="82">R · Restart</button></div>
<p>Other game actions and room changes are planned for W07. Audio is logged silently.</p>
<pre id="state"></pre><p>Functional py65 CPU harness with a simplified Disk II bus.
This view does not certify real hardware, video timing or an Oric reference run.</p>
<script>
async function press(code){await fetch('/key',{method:'POST',body:JSON.stringify({code})});}
document.querySelectorAll('button').forEach(b=>b.onclick=()=>press(+b.dataset.code));
window.addEventListener('keydown',e=>{const keys={ArrowLeft:8,ArrowRight:21,ArrowDown:10,ArrowUp:11,' ':32};
const code=keys[e.key]??(e.key.length===1?e.key.toUpperCase().charCodeAt(0):null);
if(code!==null){e.preventDefault();press(code);}});
let busy=false;
async function frame(){if(busy)return;busy=true;try{const r=await fetch('/frame');const j=await r.json();
document.getElementById('screen').src='data:image/png;base64,'+j.png;
document.getElementById('state').textContent=JSON.stringify({state:j.state,events:j.events.slice(-5)},null,2);
}finally{busy=false;}} frame();setInterval(frame,50);
</script></html>'''


def serve(machine, port):
    pending = deque(maxlen=16)
    class Handler(BaseHTTPRequestHandler):
        def reply(self, data, content_type='application/json'):
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Cache-Control', 'no-store')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            if self.path == '/':
                self.reply(HTML.encode(), 'text/html; charset=utf-8')
            elif self.path == '/frame':
                state = machine.frame(pending.popleft() if pending else None)
                image = png(machine.displayed_page(), machine.text_rows())
                self.reply(json.dumps({'state': state, 'events': machine.events(),
                                       'png': base64.b64encode(image).decode()}).encode())
            else:
                self.send_error(404)

        def do_POST(self):
            if self.path != '/key':
                self.send_error(404); return
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 < length <= 64:
                self.send_error(400); return
            try:
                code = json.loads(self.rfile.read(length))['code']
                if not isinstance(code, int) or not 0 <= code < 128:
                    raise ValueError()
            except (ValueError, KeyError):
                self.send_error(400); return
            pending.append(code)
            self.reply(b'{"queued":true}')

        def log_message(self, *_):
            pass
    server = HTTPServer(('127.0.0.1', port), Handler)
    print('Open http://127.0.0.1:%d — Ctrl-C stops the local harness.' % port, flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--serve', action='store_true')
    parser.add_argument('--port', type=int, default=8765)
    args = parser.parse_args()
    machine = Machine()
    initial = machine.boot()
    if args.serve:
        serve(machine, args.port)
        return
    (ROOT / 'build/room12-boot.png').write_bytes(png(machine.displayed_page(), machine.text_rows()))
    trace = [{'key': None, 'state': initial}]
    # Walk forward to floor, stop, turn right, walk to portal, crouch and stand.
    for key in [10, None, None, None, None, 32, 21, 21, None, None, None, None, None, None, 65, 32]:
        trace.append({'key': key, 'state': machine.frame(key)})
    (ROOT / 'build/room12-after.png').write_bytes(png(machine.displayed_page(), machine.text_rows()))
    result = {'method': 'executed NMOS CPU from Disk II BOOT0 $C600; functional bus',
              'rom_cold_start': 'not executed', 'real_hardware': 'not tested',
              'instructions': machine.instructions, 'stack_min_sp': machine.min_sp,
              'disk_sha256': digest((ROOT / 'build/laigle-dor.do').read_bytes()),
              'trace': trace, 'events': machine.events(), 'speaker_accesses': machine.bus.speaker_accesses,
              'page_flips': machine.bus.page_flips, 'visible_write_violations': machine.bus.visible_write_violations,
              'video_clock': 'simplified NTSC RDVBLBAR functional model; not hardware timing'}
    write_json(ROOT / 'build/execution.json', result)
    print(json.dumps({'initial': initial, 'final': machine.state(),
                      'events': machine.events(), 'report': 'build/execution.json'}, indent=2))


if __name__ == '__main__':
    main()
