PYTHON ?= python3
VIDEO ?= mono
GAME_VIDEO ?= dhgr
GAME_PORT ?= $(if $(filter mono,$(GAME_VIDEO)),8769,8768)
.PHONY: bootstrap build test run clean game test-game run-game game-mono test-game-mono run-game-mono games
bootstrap:
	$(PYTHON) tools/bootstrap.py
build:
	$(PYTHON) tools/build.py --video $(VIDEO)
test: build
	$(PYTHON) tools/check.py --video $(VIDEO)
run: build
	$(PYTHON) tools/run.py --serve --video $(VIDEO)
game:
	$(PYTHON) tools/build_game.py --video $(GAME_VIDEO)
test-game: game
	$(PYTHON) tools/check_game.py --video $(GAME_VIDEO)
run-game: game
	LAIGLE_STAGE=game $(PYTHON) tools/run.py --video $(GAME_VIDEO) --serve --port $(GAME_PORT)
game-mono:
	$(PYTHON) tools/build_game.py --video mono
test-game-mono: game-mono
	$(PYTHON) tools/check_game.py --video mono
run-game-mono: game-mono
	LAIGLE_STAGE=game $(PYTHON) tools/run.py --video mono --serve --port 8769
games: game game-mono
clean:
	$(PYTHON) -c "import shutil; shutil.rmtree('build', ignore_errors=True)"
