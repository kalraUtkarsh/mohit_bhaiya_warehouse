"""Flask application factory."""

import time
from importlib import import_module
import logging
import logging.config

from flask import Flask

from warehouse.extensions import mongo, login_manager
from warehouse.blueprints import all_blueprints


def create_app(config='config.py'):
    """Create Flask application with given configuration"""
    app = Flask(__name__, static_folder=None)
    app.config.from_pyfile(config)

    # Import DB models. Flask-SQLAlchemy doesn't do this automatically.
    with app.app_context():
        import_module('warehouse.models')

    # Initialize extensions/add-ons/plugins.
    mongo.init_app(app)
    login_manager.init_app(app)

    for blueprint in all_blueprints:
        import_module(blueprint.import_name)
        app.register_blueprint(blueprint)

    return app
