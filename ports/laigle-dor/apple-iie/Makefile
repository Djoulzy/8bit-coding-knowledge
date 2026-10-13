PYTHON ?= python3
VIDEO ?= mono
.PHONY: bootstrap build test run clean game test-game run-game
bootstrap:
	$(PYTHON) tools/bootstrap.py
build:
	$(PYTHON) tools/build.py --video $(VIDEO)
test: build
	$(PYTHON) tools/check.py --video $(VIDEO)
run: build
	$(PYTHON) tools/run.py --serve --video $(VIDEO)
game:
	$(PYTHON) tools/build_game.py
test-game: game
	$(PYTHON) tools/check_game.py
run-game: game
	LAIGLE_STAGE=game $(PYTHON) tools/run.py --video dhgr --serve --port 8768
clean:
	$(PYTHON) -c "import shutil; shutil.rmtree('build', ignore_errors=True)"
