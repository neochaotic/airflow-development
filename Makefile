# Makefile for Local Airflow Environment

# Default command: show help
.DEFAULT_GOAL := help

# Use bash for all shell commands
SHELL := /bin/bash

# This prefix ensures the .env file is loaded for all docker-compose commands,
# making the Makefile more robust and independent of the shell's state.
DC_PREFIX := set -a; source .env; set +a;

# Build the custom Airflow image defined in docker-compose.yaml
build:
	$(DC_PREFIX) docker-compose build

# Start all services in detached mode
up:
	$(DC_PREFIX) docker-compose up -d

# Stop and remove all services, networks, and volumes
down:
	$(DC_PREFIX) docker-compose down -v

# Restart services
restart: down up

# View logs for all services
logs:
	$(DC_PREFIX) docker-compose logs -f

# Access the Airflow CLI as root to avoid permission issues with mounted files.
cli:
	@echo "Accessing Airflow CLI..."
	$(DC_PREFIX) docker-compose run --rm --user root airflow-cli bash

# Clean up all Docker resources associated with this project
clean:
	$(DC_PREFIX) docker-compose down -v --remove-orphans
	docker image prune -f

# Run linting and formatting checks inside the consistent test environment
lint:
	@echo "Running linters and formatters..."
	$(DC_PREFIX) docker-compose build ci-test-runner
	$(DC_PREFIX) docker-compose run --rm ci-test-runner pre-commit run --all-files

# Run unit tests on the live, running environment. Faster, but relies on volume mounts.
test-local:
	@echo "Running unit tests on the local running environment..."
	$(DC_PREFIX) docker-compose run --rm --user root airflow-cli pytest -v -rA -p no:cacheprovider -m "unit" tests/

# Run unit tests using a dedicated, CI-like build-and-run strategy. Slower but more reliable.
test-ci:
	@echo "Building the dedicated test image..."
	$(DC_PREFIX) docker-compose build ci-test-runner
	@echo "Running unit tests inside the new image..."
	$(DC_PREFIX) docker-compose run --rm ci-test-runner pytest -v -rA -p no:cacheprovider -m "unit" /opt/airflow/tests/

# Run integration tests against a live GCP environment.
# This uses the 'airflow-cli' service which has local GCP credentials mounted.
test-integration:
	@echo "Running GCP integration tests..."
	$(DC_PREFIX) docker-compose run --rm --user root airflow-cli pytest -v -rA -p no:cacheprovider -m "integration" tests/

# Default test command, runs the faster local tests.
test:
	@echo "Running the default test suite (local mode)..."
	@$(MAKE) test-local

# Display this help message
help:
	@echo "Usage: make [command]"
	@echo ""
	@echo "Commands:"
	@echo "  build      Build or rebuild the custom Airflow Docker image."
	@echo "  up         Start the Airflow environment in the background."
	@echo "  down       Stop and remove containers, networks, and volumes."
	@echo "  restart    Restart the Airflow environment."
	@echo "  logs       Follow the logs of all services."
	@echo "  cli        Access the Airflow CLI container."
	@echo "  clean      Stop services and clean up all Docker resources."
	@echo "  lint       Run code linting and formatting checks."
	@echo "  test       Run unit tests on the live container (faster, for quick checks)."
	@echo "  test-local An alias for 'test'."
	@echo "  test-ci    Run the full, CI-like unit test suite (slower, more reliable)."
	@echo "  test-integration Runs integration tests against GCP using your local credentials."
	@echo ""

.PHONY: build up down restart logs cli clean help lint test test-local test-ci test-integration