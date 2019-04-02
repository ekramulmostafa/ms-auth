"""This creates flask app and configure other app attributes."""
import os
from flask import Flask

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_bcrypt import Bcrypt
import json_logging
from flask_mail import Mail, Message

from app.config import config_by_name

flask_bcrypt = Bcrypt()

# app.app_context().push()


def create_app():
    """Creating flask app and setting all modeuls and config."""

    config = config_by_name[os.getenv('APP_SETTINGS', 'dev')]
    flask_app = Flask(__name__, static_folder=None, instance_relative_config=True)
    flask_app.config.from_object(config)
    with flask_app.app_context():
        app_manager = Manager(flask_app)

        from app.models import db, ma
        db.init_app(flask_app)
        Migrate(flask_app, db)
        app_manager.add_command('db', MigrateCommand)
        ma.init_app(flask_app)

        from app.service import mail
        mail.init_app(flask_app)

        from app.api import blueprint_api
        flask_app.register_blueprint(blueprint_api)

        json_logging.ENABLE_JSON_LOGGING = True
        json_logging.COMPONENT_NAME = 'MS-Auth'
        json_logging.COMPONENT_ID = 1
        json_logging.init(framework_name='flask')
        json_logging.init_request_instrument(flask_app)

    return flask_app, app_manager


app, manager = create_app()
