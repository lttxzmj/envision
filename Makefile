.PHONY: install-deps compile-deps initdb fillup

install-deps:
	pip install -r requirements.txt

compile-deps:
	pip-compile requirements.in

initdb:
	python manage.py syncdb -dv

fillup:
	python -m tests.fixtures.posts
