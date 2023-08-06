-include .env
export

dev.install:
	@flit install --deps develop --symlink

build:
	@flit build --no-setup-py

publish:
	@flit publish

run:
	@python -m aquaparser data/report.pdf

lint:
	@mypy aquaparser
	@flake8 aquaparser
