PYTHON ?= python3
.PHONY: bootstrap build test run clean
bootstrap:
	$(PYTHON) tools/bootstrap.py
build:
	$(PYTHON) tools/build.py
test: build
	$(PYTHON) tools/check.py
run: build
	$(PYTHON) tools/run.py --serve
clean:
	$(PYTHON) -c "import shutil; shutil.rmtree('build', ignore_errors=True)"
