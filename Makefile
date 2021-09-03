source_dir := $(CURDIR)/src
tests_dir := $(CURDIR)/tests_dir
build_dir := $(CURDIR)/build
dist_dir := $(CURDIR)/dist

PYTHONPATH += $(source_dir)
ENV_NAME ?= env
PIPENV_PACKAGE ?=
# make_env = python -m venv $(ENV_NAME)
make_env = pipenv install $(PIPENV_PACKAGE)
env_dir = $(CURDIR)/$(ENV_NAME)
bin_dir = $(env_dir)/bin
activate_env = . $(bin_dir)/activate
dotenv_file = .env

STAGE ?= dev
CONFIG_VARIABLE_NAME = PAYCHECK_SETTINGS
CONFIG_FILENAME = $(CURDIR)/$(STAGE)-settings.cfg

define create-venv
	@echo Creating $@...
	$(make_env)
endef

env:
	$(create-venv)

.PHONY: install
install: env

.PHONY: run
run: create_table
	pipenv run python code/app.py

.PHONY: create_table
create_table:
	pipenv run python code/create_table.py