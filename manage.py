#!/usr/bin/env python

from __future__ import unicode_literals, absolute_import, print_function

import sys

from flask_script import Manager, prompt_pass

from envision.app import create_app
from envision.ext import db
from envision.models.post import Post
from envision.models.user import User


app = create_app()
manager = Manager(app)


@manager.shell
def context():
    return {'db': db, 'Post': Post, 'User': User}


@manager.command
def syncdb(destory=False, verbose=False):
    """Creates or destroys the database."""
    db.engine.echo = bool(verbose)
    if destory:
        db.drop_all()
    db.create_all()


@manager.command
def useradd(email):
    """Creates new user."""
    if User.get_by_email(email):
        abort('[%s] exists' % email)
    try:
        password = prompt_pass('Password [%s]' % email)
    except KeyboardInterrupt:
        abort('nothing changed.')
    user = User.create(email, password, is_active=True)
    db.session.commit()
    print('[%s:%s] is created.' % (user.id, user.email))


def abort(text, code=1):
    print(text, file=sys.stderr)
    sys.exit(code)


if __name__ == '__main__':
    manager.run()
