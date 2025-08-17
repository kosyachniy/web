include .env

.PHONY: help
help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@echo '  up          Start local development (base + local overrides)'
	@echo '  up-dev      Start development environment (base + dev overrides)'
	@echo '  up-prod     Start production environment (base + prod overrides)'
	@echo '  up-test     Start test environment (base + test overrides)'
	@echo '  up-base     Start base containers only (redis, db)'
	@echo ''
	@echo '  down        Stop local development'
	@echo '  down-dev    Stop development environment'
	@echo '  down-prod   Stop production environment'
	@echo '  down-test   Stop test environment'
	@echo '  down-base   Stop base containers only'
	@echo ''
	@echo '  test        Run all tests (API + Web)'
	@echo '  test-api    Run API tests only'
	@echo '  test-web    Run web tests only'
	@echo ''
	@echo '  lint        Run linter on all Python files'
	@echo '  unit-test   Run unit tests'
	@echo ''
	@echo '  logs        Show production logs'
	@echo '  logs-dev    Show development logs'
	@echo '  logs-api    Show API logs'
	@echo '  logs-jobs   Show jobs logs'
	@echo '  logs-tg     Show Telegram bot logs'
	@echo ''
	@echo '  shell       Connect to API container'
	@echo '  db-shell    Connect to database'
	@echo '  status      Show container status'
	@echo ''
	@echo '  clean       Clean Python cache files'
	@echo '  clean-logs  Clean log files'
	@echo '  clean-all   Clean everything'

# Start services
up:
	cd infra/compose && docker compose --env-file ../../.env -f docker-compose.yml -f docker-compose.local.yml -p ${PROJECT_NAME} up --build

up-dev:
	cd infra/compose && docker compose --env-file ../../.env -f docker-compose.yml -f docker-compose.dev.yml -p ${PROJECT_NAME} up --build

up-prod:
	cd infra/compose && docker compose --env-file ../../.env -f docker-compose.yml -f docker-compose.prod.yml -p ${PROJECT_NAME} up --build -d

up-test:
	cd infra/compose && docker compose --env-file ../../.env -f docker-compose.yml -f docker-compose.test.yml -p ${PROJECT_NAME} up --build

up-base:
	cd infra/compose && docker compose --env-file ../../.env -f docker-compose.base.yml -p ${PROJECT_NAME} up --build -d

# Stop services
down:
	cd infra/compose && docker compose --env-file ../../.env -f docker-compose.yml -f docker-compose.local.yml -p ${PROJECT_NAME} down

down-dev:
	cd infra/compose && docker compose --env-file ../../.env -f docker-compose.yml -f docker-compose.dev.yml -p ${PROJECT_NAME} down

down-prod:
	cd infra/compose && docker compose --env-file ../../.env -f docker-compose.yml -f docker-compose.prod.yml -p ${PROJECT_NAME} down

down-test:
	cd infra/compose && docker compose --env-file ../../.env -f docker-compose.yml -f docker-compose.test.yml -p ${PROJECT_NAME} down

down-base:
	cd infra/compose && docker compose --env-file ../../.env -f docker-compose.base.yml -p ${PROJECT_NAME} down

# Status and monitoring
status:
	docker ps --filter name="^${PROJECT_NAME}" --format "table {{.ID}}\t{{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"

# Run tests
test:
	cd infra/compose && docker compose --env-file ../../.env -f docker-compose.test-api.yml -p ${PROJECT_NAME} up --build --exit-code-from test
	cd infra/compose && docker compose --env-file ../../.env -f docker-compose.test-web.yml -p ${PROJECT_NAME} up --build --exit-code-from test

test-api:
	cd infra/compose && docker compose --env-file ../../.env -f docker-compose.test-api.yml -p ${PROJECT_NAME} up --build --exit-code-from test

test-web:
	cd infra/compose && docker compose --env-file ../../.env -f docker-compose.test-web.yml -p ${PROJECT_NAME} up --build --exit-code-from test

# Logs
logs:
	cd infra/compose && docker compose --env-file ../../.env -f docker-compose.yml -f docker-compose.prod.yml logs

logs-dev:
	cd infra/compose && docker compose --env-file ../../.env -f docker-compose.yml -f docker-compose.dev.yml logs

logs-local:
	cd infra/compose && docker compose --env-file ../../.env -f docker-compose.yml -f docker-compose.local.yml logs

logs-base:
	cd infra/compose && docker compose --env-file ../../.env -f docker-compose.base.yml logs

# Service-specific logs
logs-api:
	tail -f ${DATA_PATH}/logs/api.log

logs-jobs:
	tail -f ${DATA_PATH}/logs/jobs.log

logs-tg:
	tail -f ${DATA_PATH}/logs/tg.log

logs-web:
	docker service logs -f ${PROJECT_NAME}_web

# Development tools
shell:
	docker exec -it `docker ps -a | grep ${PROJECT_NAME}-api | cut -d ' ' -f 1` bash

script:
	docker exec -it `docker ps -a | grep ${PROJECT_NAME}-api | cut -d ' ' -f 1` python -m scripts.$(name)

db-shell:
	docker exec -it `docker ps -a | grep ${PROJECT_NAME}-db | cut -d ' ' -f 1` mongosh -u ${MONGO_USER} -p ${MONGO_PASS}

# Code quality
lint:
	find . -type f -name '*.py' \
	| grep -vE 'env/' \
	| grep -vE 'tests/' \
	| grep -vE 'usr/' \
	| grep -vE 'etc/' \
	| xargs pylint -f text \
		--rcfile=tests/.pylintrc \
		--msg-template='{path}:{line}:{column}: [{symbol}] {msg}'

lint-changed:
	git status -s \
	| grep -vE 'tests/' \
	| grep '\.py$$' \
	| awk '{print $$1,$$2}' \
	| grep -i '^[ma]' \
	| awk '{print $$2}' \
	| xargs pylint -f text \
		--rcfile=tests/.pylintrc \
		--msg-template='{path}:{line}:{column}: [{symbol}] {msg}'

unit-test:
	pytest -s tests/

unit-test-changed:
	git status -s \
	| grep 'tests/.*\.py$$' \
	| awk '{print $$1,$$2}' \
	| grep -i '^[ma]' \
	| awk '{print $$2}' \
	| xargs pytest -s

# Cleanup
clean:
	rm -rf env/
	rm -rf **/env/
	rm -rf __pycache__/
	rm -rf **/__pycache__/
	rm -rf .pytest_cache/
	rm -rf **/.pytest_cache/

clean-logs:
	rm -rf ${DATA_PATH}/logs/
	mkdir ${DATA_PATH}/logs/
	touch ${DATA_PATH}/logs/jobs.log ${DATA_PATH}/logs/jobs.err ${DATA_PATH}/logs/api.log ${DATA_PATH}/logs/api.err ${DATA_PATH}/logs/tg.err ${DATA_PATH}/logs/tg.log ${DATA_PATH}/logs/nginx.log ${DATA_PATH}/logs/nginx.err ${DATA_PATH}/logs/mongodb.log

clean-all:
	make clean
	make clean-logs

set:
	sudo chmod 0755 ~
	sudo chmod -R a+w ~/data/
	sudo chmod 0700 ~/.ssh
	sudo chmod -R 0600 ~/.ssh/*
	export EXTERNAL_HOST=${EXTERNAL_HOST} WEB_PORT=${WEB_PORT} API_PORT=${API_PORT} TG_PORT=${TG_PORT} DATA_PATH=${DATA_PATH} PROMETHEUS_PORT=${PROMETHEUS_PORT} GRAFANA_PORT=${GRAFANA_PORT}; \
	envsubst '$${EXTERNAL_HOST} $${WEB_PORT} $${API_PORT} $${TG_PORT} $${DATA_PATH} $${PROMETHEUS_PORT} $${GRAFANA_PORT}' < infra/nginx/prod.conf > /etc/nginx/sites-enabled/${PROJECT_NAME}.conf
	sudo systemctl restart nginx
	sudo certbot --nginx
