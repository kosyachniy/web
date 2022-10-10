include .env

PYTHON := env/bin/python

setup:
	python3 -m venv env
	$(PYTHON) -m pip install -U --force-reinstall pip
	$(PYTHON) -m pip install -r api/requirements.txt

setup-tests:
	make setup
	$(PYTHON) -m pip install -r tg/requirements.txt
	$(PYTHON) -m pip install -r tests/requirements.txt

dev:
	docker-compose -p ${PROJECT_NAME} up --build

run:
	docker-compose -f compose.prod.yml -p ${PROJECT_NAME} up --build -d

check:
	docker ps --filter name="^${PROJECT_NAME}_" --format "table {{.ID}}\t{{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"

stop:
	docker-compose -f compose.prod.yml -p ${PROJECT_NAME} stop

log:
	docker-compose -f compose.prod.yml logs

log-api:
	tail -f data/logs/api.log

log-jobs:
	tail -f data/logs/jobs.log

log-web:
	docker service logs -f ${PROJECT_NAME}_web

log-tg:
	tail -f data/logs/tg.log

connect:
	docker exec -it `docker ps -a | grep ${PROJECT_NAME}/api | cut -d ' ' -f 1` bash

test-linter-all:
	find . -type f -name '*.py' \
	| grep -vE 'env/' \
	| grep -vE 'tests/' \
	| xargs $(PYTHON) -m pylint -f text \
		--rcfile=tests/.pylintrc \
		--msg-template='{path}:{line}:{column}: [{symbol}] {msg}'

test-linter:
	git status -s \
	| grep -vE 'tests/' \
	| grep '\.py$$' \
	| awk '{print $$1,$$2}' \
	| grep -i '^[ma]' \
	| awk '{print $$2}' \
	| xargs $(PYTHON) -m pylint -f text \
		--rcfile=tests/.pylintrc \
		--msg-template='{path}:{line}:{column}: [{symbol}] {msg}'

test-unit-all:
	$(PYTHON) -m pytest -s tests/

test-unit:
	git status -s \
	| grep 'tests/.*\.py$$' \
	| awk '{print $$1,$$2}' \
	| grep -i '^[ma]' \
	| awk '{print $$2}' \
	| xargs $(PYTHON) -m pytest -s

test:
	make test-linter-all
	make test-unit-all

clear:
	rm -rf env/
	rm -rf **/env/
	rm -rf __pycache__/
	rm -rf **/__pycache__/
	rm -rf .pytest_cache/
	rm -rf **/.pytest_cache/

clear-all:
	make clear
	rm -rf **/*.err
	rm -rf **/*.log

clear-logs:
	rm -rf ${DATA_PATH}/logs/
	mkdir ${DATA_PATH}/logs/
	touch ${DATA_PATH}/logs/jobs.log ${DATA_PATH}/logs/jobs.err ${DATA_PATH}/logs/api.log ${DATA_PATH}/logs/api.err ${DATA_PATH}/logs/tg.err ${DATA_PATH}/logs/tg.log ${DATA_PATH}/logs/nginx.log ${DATA_PATH}/logs/nginx.err ${DATA_PATH}/logs/mongodb.log

set:
	sudo chmod -R 777 /root
	export EXTERNAL_HOST=${EXTERNAL_HOST} WEB_PORT=${WEB_PORT} API_PORT=${API_PORT} TG_PORT=${TG_PORT} DATA_PATH=${DATA_PATH} PROMETHEUS_PORT=${PROMETHEUS_PORT} GRAFANA_PORT=${GRAFANA_PORT} CADVISOR_PORT=${CADVISOR_PORT}; \
	envsubst '$${EXTERNAL_HOST} $${WEB_PORT} $${API_PORT} $${TG_PORT} $${DATA_PATH} $${PROMETHEUS_PORT} $${GRAFANA_PORT} $${CADVISOR_PORT}' < configs/nginx.prod.conf > /etc/nginx/sites-enabled/${PROJECT_NAME}.conf
	sudo systemctl restart nginx
	sudo certbot --nginx
