test-linter:
	find . -type f -name '*.py' \
	| grep -vE 'env/' \
	| xargs api/env/bin/pylint -f text \
	    --msg-template='{path}:{line}:{column}: [{symbol}] {msg}'
