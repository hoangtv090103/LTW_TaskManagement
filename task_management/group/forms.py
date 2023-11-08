from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired

from task_management.models import User


class GroupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    users = SelectMultipleField('Users', coerce=int)
    submit = SubmitField('Create Group')

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        self.users.choices = [(user.id, user.username) for user in User.query.all()]
