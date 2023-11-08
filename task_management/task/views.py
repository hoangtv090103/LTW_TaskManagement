from flask import Blueprint, render_template, redirect, url_for, flash
from flask import jsonify, request
from flask_login import current_user

from task_management import db
from task_management.models import Task
from task_management.task.forms import TaskForm

task_blueprint = Blueprint('tasks', __name__, template_folder='templates', static_folder='static')


@task_blueprint.route('/')
def tasks():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    tasks = Task.query.all()
    return render_template('task_list.html', tasks=tasks, view_type='list')


@task_blueprint.route('/new', methods=['POST', 'GET'])
def new_task():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(name=form.name.data, description=form.description.data,
                    priority=form.priority.data, sequence=form.sequence.data, status=form.status.data,
                    project_id=form.project_id.data, user_ids=form.user_ids.data)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('tasks.tasks'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a task: {err_msg}', category='danger')
    return render_template('task_new.html', form=form)


@task_blueprint.route('/<int:task_id>')
def task_by_id(task_id: int):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    task = Task.query.get(task_id)
    return render_template('task_detail.html', task=task)


# `/tasks/${taskId}/edit
@task_blueprint.route('/<int:task_id>/edit', methods=['POST', 'GET'])
def update_task_status(task_id):
    data = request.get_json()
    task_id = data.get('taskId')
    new_status = data.get('newStatus')

    # Update the task status in your database
    task = Task.query.get(task_id)
    if task:
        task.status = new_status
        db.session.commit()
        return jsonify({"message": "Task status updated successfully"})
    else:
        return jsonify({"error": "Task not found"}, 404)
