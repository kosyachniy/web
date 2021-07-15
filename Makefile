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
