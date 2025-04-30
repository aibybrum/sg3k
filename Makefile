MAKEFLAGS := --no-print-directory --silent

default: help

help:
	@echo "Please use 'make <target>' where <target> is one of"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z\._-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

c: copy
copy: ## Copy the example-environement file
	@cp .env-example .env

dc: docker-compose-up
docker-compose-up: ## Start Docker Compose
	@echo "Starting Docker Compose"
	@docker-compose up -d