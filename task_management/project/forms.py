from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired

from task_management.models import User


class ProjectForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    sequence = IntegerField('Sequence', validators=[DataRequired()])
    manager_id = SelectField('Project Manager', coerce=int)
    submit = SubmitField('Save')

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.manager_id.choices = [(user.id, user.username) for user in User.query.all()]
