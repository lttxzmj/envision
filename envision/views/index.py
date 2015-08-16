from __future__ import unicode_literals, absolute_import, print_function

from flask import Blueprint, render_template, abort

from envision.models.post import Post


bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    posts = Post.get_latest_multi()
    return render_template('index.html', posts=posts)


@bp.route('/post/<slug>')
def post(slug):
    post = Post.get_by_slug(slug) or abort(404)
    return render_template('post.html', post=post)
