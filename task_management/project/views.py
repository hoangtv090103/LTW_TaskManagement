from flask import Blueprint
from flask import render_template, redirect, url_for
from flask_login import current_user

from task_management.forms import *
from task_management.models import *

project_blueprint = Blueprint('projects', __name__, template_folder='templates', static_folder='static')


@project_blueprint.route('/', methods=['POST', 'GET'])
def projects():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    projects = Project.query.all()
    return render_template('project_list.html', projects=projects)


@project_blueprint.route('/new', methods=['POST', 'GET'])
def new_project():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(name=form.name.data, description=form.description.data, sequence=form.sequence.data,
                          manager_id=form.manager_id.data)
        db.session.add(project)
        db.session.commit()
        return redirect(url_for('projects.projects'))
    return render_template('project_new.html', form=form)


@project_blueprint.route('/<int:id>', methods=['POST', 'GET'])
def project_by_id(id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    project = db.get_or_404(Project, ident=id)
    return render_template('project_list.html', project=project)
