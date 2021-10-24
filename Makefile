# ============
# Main targets
# ============


# -------------
# Configuration
# -------------

$(eval venvpath     := .venv)
$(eval pip          := $(venvpath)/bin/pip)
$(eval python       := $(venvpath)/bin/python)
$(eval pytest       := $(venvpath)/bin/pytest)
$(eval bumpversion  := $(venvpath)/bin/bump2version)
$(eval twine        := $(venvpath)/bin/twine)
$(eval sphinx       := $(venvpath)/bin/sphinx-build)
$(eval isort        := $(venvpath)/bin/isort)
$(eval black        := $(venvpath)/bin/black)
$(eval gribmagic    := $(venvpath)/bin/gribmagic)

# Setup Python virtualenv
setup-virtualenv:
	@test -e $(python) || python3 -m venv --system-site-packages $(venvpath)


# -------
# Testing
# -------

# Run the main test suite
test: install-tests
	@echo "==================="
	@echo "Invoking test suite"
	@echo "==================="
	@$(pytest) -vvv tests ${ARGS}

test-parallel:
	@$(MAKE) test ARGS=--numprocesses=auto

test-refresh: install-tests test

test-junit: install-tests
	@$(pytest) tests --junit-xml .pytest_results/pytest.xml

test-coverage: install-tests
	@echo "==================="
	@echo "Invoking test suite"
	@echo "==================="
	@$(pytest) -vvv tests \
		--cov=gribmagic --cov-branch \
		--cov-report=term-missing \
		--cov-report=html:.pytest_results/htmlcov \
		--cov-report=xml:.pytest_results/coverage.xml \
		--junit-xml=.pytest_results/pytest.xml \
		${ARGS}

test-coverage-parallel:
	@$(MAKE) test-coverage ARGS=--numprocesses=auto


# ----------------------
# Linting and Formatting
# ----------------------
format: install-releasetools
	@echo "Running isort"
	@$(isort) gribmagic tests
	@echo "Running black"
	@$(black) gribmagic tests


# -------
# Release
# -------

# Release this piece of software
# Synopsis:
#   make release bump=minor  (major,minor,patch)
release: bumpversion push sdist pypi-upload


# -------------
# Documentation
# -------------

# Build the documentation
docs-html: install-doctools
	touch doc/index.rst
	export SPHINXBUILD="`pwd`/$(sphinx)"; cd doc; make html


# ===============
# Utility targets
# ===============
bumpversion: install-releasetools
	@$(bumpversion) $(bump)

push:
	git push && git push --tags

sdist:
	@$(python) setup.py sdist

pypi-upload: install-releasetools
	@$(twine) upload --skip-existing dist/*.tar.gz

install-doctools: setup-virtualenv
	@$(pip) install --quiet --requirement requirements-docs.txt --upgrade

install-releasetools: setup-virtualenv
	@$(pip) install --quiet --requirement requirements-dev.txt --upgrade

install-tests: setup-virtualenv testdata-download testoutput-clean

	@mkdir -p .pytest_results

	@echo "========================================"
	@echo "Installing/upgrading sandbox environment"
	@echo "========================================"
	@$(pip) install --quiet --editable=.[test,plotting] --upgrade
	@$(MAKE) magics-info
	@echo

	@echo "=============================="
	@echo "Installing DWD GRIB Downloader"
	@echo "=============================="
	@$(gribmagic) install dwd-grib-downloader
	@echo


# ==============
# Custom targets
# ==============
include gribmagic.mk
