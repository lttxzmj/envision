from __future__ import unicode_literals, absolute_import, print_function

from flask import Blueprint, render_template


bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    return render_template('index.html')
