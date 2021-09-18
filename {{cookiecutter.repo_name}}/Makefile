.DEFAULT_GOAL := help
MAKEFLAGS += --no-print-directory

# You can set these variables from the command line, and also from the environment for the first two.
SOURCEDIR     = source
BUILDDIR      = build
MAKE          = make
VERSION       = $(shell cat VERSION)

app_root = .
pkg_src =  $(app_root)/{{cookiecutter.package_name}}
tests_src = $(app_root)/tests

# pipx installed globals
isort = isort --multi-line=3 --trailing-comma --force-grid-wrap=0 --combine-as --line-width 88 $(pkg_src) $(tests_src)
black = black $(pkg_src) $(tests_src)
mypy = mypy $(pkg_src)
tox = tox
pipenv = pipenv
#mypy = mypy --config-file $(app_root)/mypy.ini $(pkg_src)

.PHONY: clean
clean:  ## - clean all files using .gitignore rules
	@echo "Cleaning up..."
	#@git clean -X -f -d
	rm -rf dist


.PHONY: tox
tox:   ## Run tox
	$(tox)


.PHONY: test
test:  ## - run tests
	@python -m pytest tests


.PHONY: coverage
coverage:  ## - perform test coverage checks
	python -m coverage erase
	python -m coverage run --include=$(pkg_src)/* -m pytest -ra
	#python -m coverage report -m
	python -m coverage html
	open htmlcov/index.html  # work on macOS


.PHONY: format
format:  ## - perform code style format
	@black src/{{cookiecutter.package_name}} tests


.PHONY: check-format
check-format:  ## - check code format compliance
	@black --check src/{{cookiecutter.package_name}} tests


.PHONY: sort-imports
sort-imports:  ## - apply import sort ordering
	@isort . --profile black


.PHONY: check-sort-imports
check-sort-imports:  ## - check imports are sorted
	@isort . --check-only --profile black


.PHONY: style
style: sort-imports format  ## - perform code style format


.PHONY: check-style
check-style: check-sort-imports check-format  ## - check code style compliance


.PHONY: check-types
check-types:  ## - check type hint annotations
	@cd src; mypy -p {{cookiecutter.package_name}} --ignore-missing-imports


.PHONY: check-lint
check-lint:  ## - run static analysis checks
	@pylint --rcfile=.pylintrc {{cookiecutter.package_name}} ./tests setup.py ./examples


.PHONY: check-static-analysis
check-static-analysis: check-lint check-types  ## - check code style compliance


.PHONY: build
build: clean style  ## format and build
	@echo "building"
	python -m build

.PHONY: dist
dist:  ## - create a wheel distribution package
	@python setup.py bdist_wheel


.PHONY: dist-test
dist-test: dist  ## - test a wheel distribution package
	@cd dist && ../tests/test-dist.bash ./{{cookiecutter.package_name}}-*-py3-none-any.whl


.PHONY: upload
upload:  ## upload
	@echo "upload"
	twine upload --verbose dist/*

.PHONY: tag
tag:  ## tag
	@echo "tagging $(VERSION)"
	git tag -a $(VERSION) -m "version $(VERSION)"
	git push --tags

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
help: ## Show help message
	@IFS=$$'\n' ; \
	help_lines=(`fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##/:/'`); \
	printf "%s\n\n" "Usage: make [task]"; \
	printf "%-20s %s\n" "task" "help" ; \
	printf "%-20s %s\n" "------" "----" ; \
	for help_line in $${help_lines[@]}; do \
		IFS=$$':' ; \
		help_split=($$help_line) ; \
		help_command=`echo $${help_split[0]} | sed -e 's/^ *//' -e 's/ *$$//'` ; \
		help_info=`echo $${help_split[2]} | sed -e 's/^ *//' -e 's/ *$$//'` ; \
		printf '\033[36m'; \
		printf "%-20s %s" $$help_command ; \
		printf '\033[0m'; \
		printf "%s\n" $$help_info; \
	done
