import os

from flask import Flask
from flask_apscheduler import APScheduler
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(os.path.join(basedir, 'db/task_management.db'))
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

scheduler = APScheduler()

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'tranh459789@gmail.com'
app.config['MAIL_PASSWORD'] = 'rbfmlaulqlbdtyoj'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

from . import models
from . import forms
from . import routes

from .project.views import project_blueprint
from .user.views import user_blueprint
from .task.views import task_blueprint

# Register the blueprints
app.register_blueprint(user_blueprint, url_prefix='/users')
app.register_blueprint(project_blueprint, url_prefix='/projects')
app.register_blueprint(task_blueprint, url_prefix='/tasks')
