PROJECT_NAME = web
PYTHON := env/bin/python

setup:
	python3 -m venv env
	$(PYTHON) -m pip install -r api/requirements.txt

setup-tests:
	python3 -m venv env
	$(PYTHON) -m pip install -r api/requirements.txt
	$(PYTHON) -m pip install -r tests/requirements.txt

run:
	sudo docker-compose -f docker/docker-compose.yml -p ${PROJECT_NAME} up --build

deploy:
	docker-compose -f docker/docker-compose.prod.yml -p ${PROJECT_NAME} up --build

dev:
	$(PYTHON)

connect:
	sudo docker exec -it ${PROJECT_NAME}_api_1 bash

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
