#!/usr/bin/env python

from __future__ import unicode_literals, absolute_import, print_function

from flask_script import Manager

from envision.app import create_app
from envision.ext import db


app = create_app()
manager = Manager(app)


@manager.shell
def context():
    return {'db': db}


@manager.command
def syncdb(destory=False, verbose=False):
    """Creates or destroys the database."""
    db.engine.echo = bool(verbose)
    if destory:
        db.drop_all()
    db.create_all()


if __name__ == '__main__':
    manager.run()
