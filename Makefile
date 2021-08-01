PROJECT_NAME = web

setup-dev:
	cd api && \
	python3 -m venv env && \
	env/bin/pip install -r requirements.txt

setup-tests:
	cd api && \
	python3 -m venv env && \
	env/bin/pip install -r requirements.txt && \
	env/bin/pip install -r ../tests/requirements.txt

run:
	cd docker && \
	sudo docker-compose -p ${PROJECT_NAME} up --build

dev:
	cd api && \
	env/bin/python

test-linter-all:
	cd api && \
	find .. -type f -name '*.py' \
	| grep -vE 'env/' \
	| grep -vE 'tests/' \
	| xargs env/bin/python -m pylint -f text \
		--rcfile=../tests/.pylintrc \
		--msg-template='{path}:{line}:{column}: [{symbol}] {msg}'

test-linter:
	cd api && \
	git status -s \
	| grep -vE 'tests/' \
	| grep '\.py$$' \
	| awk '{print $$1,$$2}' \
	| grep -i '^[ma]' \
	| awk '{print $$2}' \
	| xargs env/bin/python -m pylint -f text \
		--rcfile=../tests/.pylintrc \
		--msg-template='{path}:{line}:{column}: [{symbol}] {msg}'

test-unit-all:
	cd api && \
	env/bin/python -m pytest ../tests/
