from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, SelectMultipleField, \
    BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Optional

from task_management.models import *


class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username.')

    def validate_email(self, email_to_check):
        email = User.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError('Email already exists! Please try a different email.')

    name = StringField('Name')
    username = StringField('Username', validators=[DataRequired()])
    password1 = PasswordField('Password', validators=[DataRequired(), EqualTo('password2')])
    password2 = PasswordField('Confirm Password', validators=[EqualTo('password1')])
    email = StringField('Email', validators=[Optional(), Email()])
    phone = StringField('Phone')
    submit = SubmitField('Create Account')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class GroupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    users = SelectMultipleField('Users', coerce=int)
    submit = SubmitField('Create Group')

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        self.users.choices = [(user.id, user.username) for user in User.query.all()]


class ProjectForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    sequence = IntegerField('Sequence', validators=[DataRequired()])
    manager_id = SelectField('Project Manager', coerce=int)
    submit = SubmitField('Create Project')

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.manager_id.choices = [(user.id, user.username) for user in User.query.all()]


class UserForm(FlaskForm):
    # __tablename__ = 'user'
    # id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(100))
    # username = db.Column(db.String(100), nullable=False)
    # password_hashed = db.Column(db.String(100), nullable=False)
    # active = db.Column(db.Boolean, default=True)
    # phone = db.Column(db.String(100))
    # email = db.Column(db.String(100))
    # created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    # updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    # create_uid = db.Column(db.Integer, default=0)
    # write_uid = db.Column(db.Integer, default=0)
    # role = db.Column(db.String(100))
    # group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    # db.UniqueConstraint(username, email)
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    active = BooleanField('Active')
    phone = StringField('Phone')
    email = StringField('Email', validators=[Optional(), Email()])
    role = SelectField('Role', choices=[('admin', 'Admin'), ('user', 'User')])
    group_id = SelectField('Group', coerce=int)
    submit = SubmitField('Create User')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.group_id.choices = [(group.id, group.name) for group in Group.query.all()]
