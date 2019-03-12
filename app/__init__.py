"""This creates flask app and configure other app attributes."""
import os
from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_bcrypt import Bcrypt

from app.config import config_by_name


flask_bcrypt = Bcrypt()
# app.app_context().push()


def create_app():
    """Creating flask app and setting all modeuls and config."""
    flask_app = Flask(__name__, static_folder=None, instance_relative_config=True)
    flask_app.config.from_object(config_by_name[os.getenv('APP_SETTINGS', 'dev')])
    app_manager = Manager(flask_app)

    from app.models import db, ma
    db.init_app(flask_app)
    Migrate(flask_app, db)
    app_manager.add_command('db', MigrateCommand)
    ma.init_app(flask_app)

    from app.api import blueprint_api
    flask_app.register_blueprint(blueprint_api)

    return flask_app, app_manager


app, manager = create_app()
