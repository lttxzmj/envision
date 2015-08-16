from __future__ import unicode_literals, absolute_import, print_function

from uuid import uuid4
from datetime import datetime

from enum import Enum
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy_utils import UUIDType, ChoiceType

from envision.ext import db
from envision.models.user import User


class Post(db.Model):
    """The posts or articles."""

    class Status(Enum):
        publish = 'P'
        draft = 'D'
        trash = 'T'

    class ContentType(Enum):
        raw_html = 0
        markdown = 1

    uuid = db.Column(UUIDType(), primary_key=True, default=uuid4)
    title = db.Column(db.Unicode(30), nullable=False)
    slug = db.Column(db.Unicode(60), nullable=False, unique=True)
    author_id = db.Column(db.Integer(), nullable=False)
    author = db.relationship(
        User, uselist=False, primaryjoin='User.id == Post.author_id',
        foreign_keys='Post.author_id')
    status = db.Column(ChoiceType(Status), default=Status.draft)
    content = db.Column(db.Unicode(512))
    content_type = db.Column(
        ChoiceType(ContentType, impl=db.Integer()),
        default=ContentType.markdown)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    @classmethod
    def create(cls, title, slug, author, status=None):
        instance = cls(title=title, slug=slug, author=author)
        if status is not None:
            instance.status = status
        return instance

    @classmethod
    def get_by_slug(cls, slug, status=None):
        try:
            instance = cls.query.filter_by(slug=slug).one()
        except NoResultFound:
            return
        else:
            if status not in (None, instance.status):
                return
            return instance

    @classmethod
    def get_latest_multi(cls, limit=10, status=Status.publish):
        query = cls.query.filter_by(status=status)
        return query.order_by(cls.created_at.desc())[:limit]

    def set_content(self, content, content_type=None):
        self.content = content
        if content_type:
            self.content_type = content_type
