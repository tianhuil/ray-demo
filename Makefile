SHELL := /bin/bash

# set variables
export NAME = ray-demo
export PYTHON = python3
export PIP = pip3
export ROOT_DIR = $(shell pwd)

create:
	$$PYTHON -m venv env

install:
	source env/bin/activate && $$PIP install -r requirements.txt
	echo "$$ROOT_DIR/src/" > $(shell ls -d env/lib/python*/site-packages)/local.pth

create-install: create install
	source env/bin/activate && ipython kernel install --user --name=$$NAME


# from https://stackoverflow.com/a/3452888/8930600
upgrade:
	source env/bin/activate && pip3 list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U

ipython:
	source env/bin/activate && ipython --pdb

jupyter:
	source env/bin/activate && cd analysis && jupyter notebook
