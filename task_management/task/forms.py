from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SelectMultipleField, SubmitField, DateField
from wtforms.validators import DataRequired

from task_management.models import Project, User


class TaskForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    priority = IntegerField('Priority', default=0)
    sequence = StringField('Sequence')
    date_start = DateField('Start Date')
    # date_end must be greater than date_start
    date_end = DateField('End Date', validators=[DataRequired()])
    status = SelectField('Status', coerce=str)
    project_id = SelectField('Project', coerce=int)
    user_ids = SelectMultipleField('User', coerce=int)
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.project_id.choices = [(project.id, project.name) for project in Project.query.all()]
        self.user_ids.choices = [(user.id, user.username) for user in User.query.all()]
        self.status.choices = [('todo', 'To Do'), ('in-progress', 'In Progress'), ('done', 'Done')]

    def validate(self, extra_validators=None):
        # Validate the date_start and date_end
        if self.date_start.data and self.date_end.data:
            if self.date_start.data > self.date_end.data:
                # errors is tuple
                self.date_start.errors = ('Start date must be less than end date')
                return False
        return super(TaskForm, self).validate()
