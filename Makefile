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

# node:
# 	docker-compose -f docker/docker-compose.metrics.yml build
# 	sudo docker stack deploy --compose-file docker/docker-compose.metrics.yml ${PROJECT_NAME}

# check:
# 	docker stack services ${PROJECT_NAME}

# stop:
# 	docker stack rm ${PROJECT_NAME}

log-api:
	tail -f data/logs/api.log

log-jobs:
	tail -f data/logs/jobs.log

log-web:
	docker service logs -f ${PROJECT_NAME}_web

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

set:
	export EXTERNAL_HOST=${EXTERNAL_HOST}; \
	envsubst '$${EXTERNAL_HOST}' < nginx.conf > /etc/nginx/sites-enabled/${PROJECT_NAME}.conf
	sudo systemctl restart nginx
	sudo certbot --nginx
