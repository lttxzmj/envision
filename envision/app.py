from __future__ import unicode_literals, absolute_import, print_function

from flask import Flask
from werkzeug.utils import import_string


extensions = [
    'envision.ext:db',
    'envision.ext:login_manager',
]
blueprints = [
]


def create_app():
    app = Flask(__name__)
    app.config.from_object('envcfg.json.envision')

    for extension_name in extensions:
        extension = import_string(extension_name)
        extension.init_app(app)

    for blueprint_name in blueprints:
        blueprint = import_string(blueprint_name)
        app.register_blueprint(blueprint)

    return app
