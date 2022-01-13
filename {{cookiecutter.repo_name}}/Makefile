.DEFAULT_GOAL := help
MAKEFLAGS += --no-print-directory

# You can set these variables from the command line, and also from the environment for the first two.
BUILDDIR      = build
MAKE          = make
VERSION       = $(shell cat VERSION)

app_root = $(PROJ_DIR)
app_root ?= .
pkg_src =  $(app_root)/{{cookiecutter.package_name}}
tests_src = $(app_root)/tests

define BROWSER_PYSCRIPT
import os, webbrowser, sys

try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("\033[36m%-20s\033[0m %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT


lint: ## check style with flake8
	flake8 {{ cookiecutter.package_name }}


.PHONY: tox
tox:   ## Run tox
	$(tox)

.PHONY: test
test:  ## run tests
	@python -m pytest tests

.PHONY: coverage
coverage:  ## perform test coverage checks
	python -m coverage erase
	python -m coverage run --source {{ cookiecutter.package_name }} -m pytest -ra
	python -m coverage report -m
	python -m coverage html
	$(BROWSER) htmlcov/index.html

.PHONY: format
format:  ## perform code style format
	@black {{cookiecutter.package_name}} tests


.PHONY: sort-imports
sort-imports:  ## apply import sort ordering
	@isort . --profile black

.PHONY: check-sort-imports
check-sort-imports:  ## check imports are sorted
	@isort . --check-only --profile black

.PHONY: style
style: sort-imports format  ## perform code style format

.PHONY: check-style
check-style: check-sort-imports check-format  ## check code style compliance

.PHONY: mypy
mypy:  ## check type hint annotations
	@mypy -p {{cookiecutter.package_name}} --ignore-missing-imports

.PHONY: build
build: clean style  ## format and build
	@echo "building"
	python -m build

.PHONY: dist
dist:  ## create a wheel distribution package
	@python setup.py sdist
	@python setup.py bdist_wheel
	ls -al dist


.PHONY: upload
upload:  ## upload
	@echo "upload"
	twine upload --verbose dist/*

.PHONY: tag
tag:  ## tag
	@echo "tagging $(VERSION)"
	git tag -a $(VERSION) -m "version $(VERSION)"
	git push --tags

.PHONY: install
install: clean build uninstall ## pipx install
	pipx install $(app_root)/{{cookiecutter.package_name}}

.PHONY: uninstall
uninstall:  ## pipx uninstall
	-pipx uninstall {{cookiecutter.package_name}}

.PHONY: bump-major
bump-major:  ## bump-major
	bumpversion --verbose major

.PHONY: bump-minor
bump-minor:  ## bump-minor
	bumpversion --verbose minor

.PHONY: bump-patch
bump-patch:  ## bump-patch
	bumpversion --verbose patch

.PHONY: help
help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

.PHONY: clean
clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

.PHONY: clean-build
clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . \( -path ./env -o -path ./venv -o -path ./.env -o -path ./.venv \) -prune -o -name '*.egg-info' -exec rm -fr {} +
	find . \( -path ./env -o -path ./venv -o -path ./.env -o -path ./.venv \) -prune -o -name '*.egg' -exec rm -f {} +

.PHONY: clean-pyc
clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

{%- if cookiecutter.use_make_confirm == 'y' %}
.PHONY: _confirm
_confirm:
	@echo -n "Are you sure? [y/N] " && read ans && [ $${ans:-N} = y ]
	@echo "Action confirmed by user."
{%- endif %}
