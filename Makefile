install-deps:
	pip install -r requirements.txt

compile-deps:
	pip-compile requirements.in
