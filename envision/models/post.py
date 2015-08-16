from __future__ import unicode_literals, absolute_import, print_function

from uuid import uuid4
from datetime import datetime

from flask import url_for
from enum import Enum
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy_utils import UUIDType, ChoiceType
from misaka import html as render_markdown
from html5lib import HTMLParser, serialize
from html5lib.sanitizer import HTMLSanitizer
from html5lib_truncation import truncate_html

from envision.ext import db
from envision.models.user import User


def render_sanitized_html(html):
    parser = HTMLParser(tokenizer=HTMLSanitizer)
    etree = parser.parse(html)
    return serialize(etree)


class Post(db.Model):
    """The posts or articles."""

    class Status(Enum):
        publish = 'P'
        draft = 'D'
        trash = 'T'

    class ContentType(Enum):
        raw_html = 0
        markdown = 1

    ContentType.raw_html.as_html = render_sanitized_html
    ContentType.markdown.as_html = render_markdown

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

    @property
    def permalink(self):
        return url_for('index.post', slug=self.slug)

    def set_content(self, content, content_type=None):
        self.content = content
        if content_type:
            self.content_type = content_type

    def as_html(self, max_length=None, ellipsis=''):
        html = self.content_type.as_html(self.content)
        if max_length is not None:
            html = truncate_html(
                html, max_length, end=ellipsis, break_words=True)
        return html
