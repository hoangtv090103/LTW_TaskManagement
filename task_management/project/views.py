from flask import Blueprint, session, jsonify
from flask import render_template, redirect, url_for
from flask_login import current_user

from task_management.models import *
from task_management.project.forms import ProjectForm
from task_management.routes import index, login_required
from task_management.task.views import get_task_list

project_blueprint = Blueprint('projects', __name__, template_folder='templates', static_folder='static')


@project_blueprint.route('/', methods=['POST', 'GET'])
@login_required
def projects():
    projects = Project.query.all()
    return render_template('project_list.html', projects=projects, view_type='list')


@project_blueprint.route('/new', methods=['POST', 'GET'])
@login_required
def new_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(name=form.name.data, description=form.description.data, sequence=form.sequence.data,
                          manager_id=current_user.id)
        db.session.add(project)
        db.session.commit()
        return index()
    return render_template('project_new.html', form=form)


@project_blueprint.route('/<int:project_id>', methods=['GET'])
@login_required
def project_by_id(project_id):
    project = db.get_or_404(Project, ident=project_id)
    session['active_project_id'] = project.id
    tasks = Task.query.filter(Task.project_id == project_id).all()
    task_list = get_task_list(tasks)
    return index(project_id=project, task_list=task_list)


@project_blueprint.route('/<int:id>/edit', methods=['POST', 'GET'])
@login_required
def edit_project(id):
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

@project_blueprint.route('/delete/<int:project_id>/', methods=['POST', 'GET', 'DELETE'])
@login_required
def delete_project(project_id):
    if project_id:
        project = Project.query.get(project_id)
        tasks = Task.query.filter(Task.project_id == project_id).all()
        if project:
            for task in tasks:
                db.session.delete(task)
            db.session.delete(project)
            db.session.commit()
            return index()
        else:
            return jsonify({"error": "Project not found"}, 404)
    else:
        return jsonify({"error": "Method not allowed"}, 405)