import os
from flask import Flask
from .models import db
from .oauth2 import config_oauth
from .routes import bp
from flask_cors import CORS


def create_app(config=None):
    app = Flask(__name__)
    CORS(app, supports_credentials=True)

    # load default configuration
    app.config.from_object('website.settings')

    # load environment configuration
    if 'WEBSITE_CONF' in os.environ:
        app.config.from_envvar('WEBSITE_CONF')

    # load app sepcified configuration
    if config is not None:
        if isinstance(config, dict):
            app.config.update(config)
        elif config.endswith('.py'):
            app.config.from_pyfile(config)

    setup_app(app)
    return app


def setup_app(app):
    db.init_app(app)
    config_oauth(app)
    app.register_blueprint(bp, url_prefix='')
