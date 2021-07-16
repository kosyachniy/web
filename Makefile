PROJECT_NAME = web

run:
	cd docker && \
	sudo docker-compose -p ${PROJECT_NAME} up --build

dev:
	cd api && \
	python3 -m venv env && \
	env/bin/pip install -r requirements.txt && \
	env/bin/python

test-linter-all:
	find . -type f -name '*.py' \
	| grep -vE 'env/' \
	| xargs python3 -m pylint -f text \
		--rcfile=.pylintrc \
		--msg-template='{path}:{line}:{column}: [{symbol}] {msg}'

test-linter:
	git status -s \
	| grep '\.py$$' \
	| awk '{print $$1,$$2}' \
	| grep -i '^[ma]' \
	| awk '{print $$2}' \
	| xargs python3 -m pylint -f text \
		--rcfile=.pylintrc \
		--msg-template='{path}:{line}:{column}: [{symbol}] {msg}'
