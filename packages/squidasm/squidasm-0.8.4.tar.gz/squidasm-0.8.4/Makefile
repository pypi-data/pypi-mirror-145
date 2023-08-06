PYTHON3        = python3
SOURCEDIR      = squidasm
TESTDIR        = tests
EXAMPLEDIR     = examples
RUNEXAMPLES    = ${EXAMPLEDIR}/run_examples.py
PIP_FLAGS      = --extra-index-url=https://${NETSQUIDPYPI_USER}:${NETSQUIDPYPI_PWD}@pypi.netsquid.org
MINCOV         = 0

help:
	@echo "install           Installs the package (editable)."
	@echo "verify            Verifies the installation, runs the linter and tests."
	@echo "tests             Runs the tests."
	@echo "examples          Runs the examples and makes sure they work."
	@echo "open-cov-report   Creates and opens the coverage report."
	@echo "lint              Runs the linter."
	@echo "bdist             Builds the package."
	@echo "test-deps         Installs the requirements needed for running tests and linter."
	@echo "python-deps       Installs the requirements needed for using the package."
	@echo "docs              Creates the html documentation"
	@echo "clean             Removes all .pyc files."

test-deps:
	@$(PYTHON3) -m pip install -r test_requirements.txt

requirements python-deps: _check_variables
	@$(PYTHON3) -m pip install -r requirements.txt ${PIP_FLAGS}

_check_variables:
ifndef NETSQUIDPYPI_USER
	$(error Set the environment variable NETSQUIDPYPI_USER before uploading)
endif
ifndef NETSQUIDPYPI_PWD
	$(error Set the environment variable NETSQUIDPYPI_PWD before uploading)
endif

clean:
	@/usr/bin/find . -name '*.pyc' -delete

lint-isort:
	$(info Running isort...)
	@$(PYTHON3) -m isort --check --diff ${SOURCEDIR} ${TESTDIR} ${EXAMPLEDIR}

lint-black:
	$(info Running black...)
	@$(PYTHON3) -m black --check ${SOURCEDIR} ${TESTDIR} ${EXAMPLEDIR}

lint-flake8:
	$(info Running flake8...)
	@$(PYTHON3) -m flake8 ${SOURCEDIR} ${TESTDIR} ${EXAMPLEDIR}

lint-mypy:
	$(info Running mypy...)
	@$(PYTHON3) -m mypy ${SOURCEDIR} ${TESTDIR}

# TODO: fix lint-isort in CI
# TODO: run lint-mypy again
# lint: lint-black lint-flake8 lint-mypy
lint: lint-black lint-flake8

tests:
	@$(PYTHON3) -m pytest --cov=${SOURCEDIR} --cov-fail-under=${MINCOV} tests

open-cov-report:
	@$(PYTHON3) -m pytest --cov=${SOURCEDIR} --cov-report html tests && open htmlcov/index.html

examples:
	@${PYTHON3} ${RUNEXAMPLES}

docs html:
	@${MAKE} -C docs html

build bdist: _clean_dist
	@$(PYTHON3) setup.py bdist_wheel

install: python-deps test-deps
	@$(PYTHON3) -m pip install -e . ${PIP_FLAGS}

_clean_dist:
	@/bin/rm -rf dist

verify: clean test-deps python-deps lint tests examples _verified

_verified:
	@echo "The snippet is verified :)"

.PHONY: clean lint test-deps python-deps tests verify bdist deploy-bdist _clean_dist install open-cov-report examples docs
