from __future__ import unicode_literals, absolute_import, print_function

from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from envision.ext import db


class User(UserMixin, db.Model):
    """The site users."""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Unicode(20), nullable=False, unique=True)
    password = db.Column(db.String(70), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create(cls, email, password, is_active=False):
        instance = cls(email=email, is_active=is_active)
        instance.change_password(password)
        db.session.add(instance)
        return instance

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def change_password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, input_password):
        return check_password_hash(self.password, input_password)

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False
