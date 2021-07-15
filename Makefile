test-linter-all:
	find . -type f -name '*.py' \
	| grep -vE 'env/' \
	| xargs python3 -m pylint -f text \
 		--rcfile=.pylintrc \
	    --msg-template='{path}:{line}:{column}: [{symbol}] {msg}'
