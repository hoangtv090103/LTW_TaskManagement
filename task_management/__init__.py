import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(os.path.join(basedir, 'db/task_management.db'))
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
from . import models
from . import forms
from . import routes

from .group.views import group_blueprint
from .project.views import project_blueprint
from .user.views import user_blueprint

# Register the blueprints
app.register_blueprint(user_blueprint, url_prefix='/users')
app.register_blueprint(group_blueprint, url_prefix='/groups')
app.register_blueprint(project_blueprint, url_prefix='/projects')
