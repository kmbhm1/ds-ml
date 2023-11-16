.PHONY: help setup activate-env deactivate-env check-venv python-version clean build update-deps jupyter data install-aws-cli check-aws-credentials sync-data-to-s3 sync-data-from-s3 pre-commit lint format check-types code-quality test test-coverage test-coverage-html test-verbose
.DEFAULT_GOAL := help

#################################################################################
# PROJECT VARIABLES                                                                      #
#################################################################################

# ANSI color codes
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
NC := \033[0m # No Color

# Project variables
PYPI_INDEX := https://test.pypi.org/legacy/
# PYPI_TOKEN should be set as an environment variable or defined here
# PYPI_TOKEN := your-pypi-token
S3_BUCKET_NAME := ds-ml
LOCAL_DATA_DIRECTORY := ./data
S3_DATA_PATH := s3://$(S3_BUCKET_NAME)/data

# System detection
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Linux)
    INSTALL_CMD = curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
                  unzip awscliv2.zip && \
                  sudo ./aws/install && \
                  rm -rf ./aws awscliv2.zip
endif
ifeq ($(UNAME_S),Darwin)
    INSTALL_CMD = brew install awscli
endif

#################################################################################
# POETRY ENV MANAGEMENT COMMANDS                                                                      #
#################################################################################

# Virtual environment management
setup:
	@echo "${GREEN}Setting up the project using Poetry...${NC}"
	@poetry install

activate-env:
	@echo "${GREEN}Activating the Poetry virtual environment...${NC}"
	@poetry shell

deactivate-env:
	@echo "${GREEN}Deactivating the Poetry virtual environment...${NC}"
	@deactivate

check-venv:
	@echo "${YELLOW}Checking if the Poetry virtual environment is active...${NC}"
	@poetry env info

python-version:
	@echo "${BLUE}Retrieving Python version used by Poetry...${NC}"
	@poetry run python --version

# Project management
clean:
	@echo "${RED}Cleaning up Python compiled directories...${NC}"
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name "htmlcov" -exec rm -rf {} +
	@find . -type d -name "*.egg-info" -exec rm -rf {} +
	@find . -type f -name "*.py[co]" -exec rm -f {} +
	@find . -type f -name "*.pyo" -exec rm -f {} +

build:
	@echo "${GREEN}Building the package...${NC}"
	@poetry build

# .PHONY: publish
# publish:
# 	@echo "${GREEN}Publishing the package to PyPI...${NC}"
# 	@poetry publish --repository $(PYPI_INDEX) --username __token__ --password $(PYPI_TOKEN)

update-deps:
	@echo "${YELLOW}Updating project dependencies...${NC}"
	@poetry update

#################################################################################
# JUPYTER                                                                    #
#################################################################################

jupyter:
	@echo "${GREEN}Starting Jupyter Notebook...${NC}"
	@poetry run jupyter notebook

#################################################################################
# PACKAGE SPECIFIC                                                                    #
#################################################################################

## Make Dataset
# data: requirements
# 	$(PYTHON_INTERPRETER) src/data/make_dataset.py data/raw data/processed

#################################################################################
# AWS MANAGEMENT COMMANDS                                                                      #
#################################################################################

install-aws-cli:
	@echo "${BLUE}Checking for AWS CLI installation...${NC}"
	@which aws >/dev/null 2>&1 || (echo "${GREEN}Installing AWS CLI...${NC}" && $(INSTALL_CMD))

check-aws-credentials:
	@if aws sts get-caller-identity > /dev/null; then \
		echo "${GREEN}AWS credentials found and valid.${NC}"; \
	else \
		echo "${YELLOW}AWS credentials not found or invalid.${NC}"; \
		echo "${YELLOW}Please run 'aws configure' to set up your credentials.${NC}"; \
		exit 1; \
	fi

sync-data-to-s3:
	@echo "${GREEN}Syncing data to the S3 bucket...${NC}"
	@aws s3 sync $(LOCAL_DATA_DIRECTORY) $(S3_DATA_PATH)

sync-data-from-s3:
	@echo "${GREEN}Syncing data from the S3 bucket...${NC}"
	@aws s3 sync $(S3_DATA_PATH) $(LOCAL_DATA_DIRECTORY)


#################################################################################
# VERSIONS                                                                 		#
#################################################################################

.PHONY: bump-patch
bump-patch:
	@echo "${YELLOW}Bumping patch version...${NC}"
	@poetry run cz bump --changelog

#################################################################################
# CODE QUALITY                                                                  #
#################################################################################

pre-commit:
	@echo "${YELLOW}Running pre-commit...${NC}"
	@poetry run pre-commit run --all-files

lint:
	@echo "${YELLOW}Running linters...${NC}"
	@echo "${YELLOW}Running ruff...${NC}"
	@poetry run ruff check --fix .

format:
	@echo "${YELLOW}Formatting code...${NC}"
	@echo "${YELLOW}Running ruff...${NC}"
	@poetry run ruff format .

check-types:
	@echo "${YELLOW}Type checking...${NC}"
	@poetry run mypy src

code-quality: lint format check-types

#################################################################################
# TESTING                                                                 #
#################################################################################

# Run all tests
test:
	@echo "${YELLOW}Running tests...${NC}"
	@poetry run pytest

# Run tests with verbose output
test-verbose:
	@echo "${YELLOW}Running tests with verbose output...${NC}"
	@poetry run pytest -v

# Run tests with coverage
test-coverage:
	@echo "${YELLOW}Running tests with coverage...${NC}"
	@poetry run pytest --cov=src --cov-report=term-missing --cov-config=pyproject.toml

# Run tests with coverage html
test-coverage-html:
	@echo "${YELLOW}Running tests with coverage...${NC}"
	@poetry run pytest --cov=src --cov-report=html --cov-config=pyproject.toml

#################################################################################
# HELP                                                                 #
#################################################################################

help:
	@echo "${GREEN}Available commands:${NC}"
	@echo "${YELLOW}  setup            		- Set up the project using Poetry${NC}"
	@echo "${YELLOW}  activate-env     		- Activate the Poetry virtual environment${NC}"
	@echo "${YELLOW}  deactivate-env   		- Deactivate the Poetry virtual environment${NC}"
	@echo "${YELLOW}  check-venv       		- Check if the Poetry virtual environment is active${NC}"
	@echo "${YELLOW}  python-version   		- Retrieve Python version used by Poetry${NC}"
	@echo "${YELLOW}  clean            		- Clean up Python compiled directories${NC}"
	@echo "${YELLOW}  build            		- Build the project package${NC}"
	@echo "${YELLOW}  publish          		- Publish the package to PyPI${NC}"
	@echo "${YELLOW}  update-deps      		- Update the project dependencies${NC}"
	@echo "${YELLOW}  jupyter          		- Start Jupyter Notebook${NC}"
	@echo "${YELLOW}  install-aws-cli  		- Install AWS CLI${NC}"
	@echo "${YELLOW}  check-aws-credentials 	- Check if AWS credentials are set up${NC}"
	@echo "${YELLOW}  sync-data-to-s3  		- Sync data to the S3 bucket${NC}"
	@echo "${YELLOW}  sync-data-from-s3  		- Sync data from the S3 bucket${NC}"
	@echo "${YELLOW}  pre-commit             	- Run pre-commit${NC}"
	@echo "${YELLOW}  lint             		- Run linters on the project${NC}"
	@echo "${YELLOW}  format           		- Format the project code${NC}"
	@echo "${YELLOW}  check-types      		- Perform type checking${NC}"
	@echo "${YELLOW}  code-quality     		- Perform all code quality checks${NC}"
	@echo "${YELLOW}  test             		- Run all tests${NC}"
	@echo "${YELLOW}  test-coverage    		- Run tests with coverage${NC}"
	@echo "${YELLOW}  test-coverage-html 		- Run tests with coverage html${NC}"
	@echo "${YELLOW}  test-verbose     		- Run tests with verbose output${NC}"
	@echo "${YELLOW}  help             		- Print this help message${NC}"
