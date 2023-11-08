from flask import Blueprint, request, session
from flask import render_template, redirect, url_for
from flask_login import current_user

from task_management.models import *
from task_management.project.forms import ProjectForm

project_blueprint = Blueprint('projects', __name__, template_folder='templates', static_folder='static')


@project_blueprint.route('/', methods=['POST', 'GET'])
def projects():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    projects = Project.query.all()
    return render_template('project_list.html', projects=projects, view_type='list')


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
        return redirect(url_for('index'))
    return render_template('project_new.html', form=form)


@project_blueprint.route('/<int:project_id>', methods=['GET'])
def project_by_id(project_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    project = db.get_or_404(Project, ident=project_id)
    session['project_id'] = project_id
    return redirect(url_for('index'))


@project_blueprint.route('/<int:id>/edit', methods=['POST', 'GET'])
def edit_project(id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    project = db.get_or_404(Project, ident=id)
    form = ProjectForm(obj=project)
    if form.validate_on_submit():
        project.name = form.name.data
        project.description = form.description.data
        project.sequence = form.sequence.data
        project.manager_id = form.manager_id.data
        db.session.commit()
        return redirect(url_for('projects.project_by_id', id=id))
    return render_template('project_edit.html', form=form, project=project)
