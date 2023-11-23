from datetime import datetime

from flask import Blueprint, render_template, flash, session
from flask import jsonify, request
from flask_login import current_user

from task_management import db
from task_management.models import Task
from task_management.routes import index, login_required
from task_management.task.forms import TaskForm

task_blueprint = Blueprint('tasks', __name__, template_folder='templates', static_folder='static')


def get_task_list(tasks):
    task_list = {
        'todo': [task for task in tasks if task.status == 'todo'],
        'in-progress': [task for task in tasks if task.status == 'in-progress'],
        'done': [task for task in tasks if task.status == 'done']
    }
    return task_list


@task_blueprint.route('/')
@login_required
def tasks():
    all_task = Task.query.filter(Task.user_id == current_user.id).all()
    task_list = get_task_list(all_task)

    return index(task_list=task_list)


@task_blueprint.route('/new', methods=['POST', 'GET'])
@login_required
def new_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(name=form.name.data, description=form.description.data,
                    priority=form.priority.data, status=form.status.data,
                    project_id=form.project_id.data, date_start=form.date_start.data,
                    date_end=form.date_end.data, user_id=current_user.id)
        db.session.add(task)
        db.session.commit()
        return index()
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a task: {err_msg}', category='danger')
    return render_template('task_new.html', form=form)


@task_blueprint.route('/<int:task_id>', methods=['POST', 'GET'])
@login_required
def task_by_id(task_id: int):
    task = Task.query.get(task_id)
    return index(task_id=task)


@task_blueprint.route('/<int:task_id>/edit', methods=['POST', 'GET', 'PUT'])
@login_required
def edit_task(task_id):
    if request.method == 'PUT':
        data = request.get_json()
        task_id = data.get('taskId')
        new_status = data.get('newState')

        task = Task.query.get(task_id)
        if task:
            task.status = new_status
            db.session.commit()
            return jsonify({"message": "Task status updated successfully"})
        else:
            return jsonify({"error": "Task not found"}, 404)

    elif request.method == 'POST':
        session['active_task_id'] = task_id
        session['mode'] = 'edit'
        return index()
    else:
        return jsonify({"error": "Method not allowed"}, 405)


def is_changed(task=None, data=None):
    if task.name != data.get('name'):
        return True
    if task.description != data.get('description'):
        return True
    if task.priority != data.get('priority'):
        return True
    if task.status != data.get('status'):
        return True
    if task.project_id != data.get('project_id'):
        return True
    if task.date_start != data.get('date_start'):
        return True
    if task.date_end != data.get('date_end'):
        return True
    if task.project_id != data.get('project_id'):
        return True
    return False


@task_blueprint.route('/<int:task_id>/save', methods=['POST'])
@login_required
def save_task(task_id):
    if request.method == 'POST':
        session.pop('mode', None)
        data = request.get_json()
        data.update({
            'date_start': datetime.strptime(data.get('date_start'), '%Y-%m-%d').date(),
            'date_end': datetime.strptime(data.get('date_end'), '%Y-%m-%d').date(),
        })
        task = Task.query.get(task_id)
        if not task:
            return jsonify({"error": "Task not found"}, 404)
        if is_changed(task, data):
            task.name = data.get('name')
            task.description = data.get('description')
            task.priority = data.get('priority')
            task.status = data.get('status')
            task.date_start = data.get('date_start')
            task.date_end = data.get('date_end')
            task.project_id = data.get('project_id')
            db.session.commit()
        return index()


@task_blueprint.route('/delete/<int:task_id>/', methods=['POST', 'GET', 'DELETE'])
@login_required
def delete_task(task_id):
    if task_id:
        task = Task.query.get(task_id)
        if task:
            db.session.delete(task)
            db.session.commit()
            return tasks()
        else:
            return jsonify({"error": "Task not found"}, 404)
    # elif request.method == 'POST':
    #     session['active_task_id'] = task_id
    #     session.pop('mode', None)
    #     return index()
    else:
        return jsonify({"error": "Method not allowed"}, 405)


@task_blueprint.route('/search', methods=['POST'])
@login_required
def search():
    if request.method == 'POST':
        keyword = request.get_json().get('keyword')
        if session.get('active_project_id'):
            project_id = session.get('active_project_id')
            tasks = Task.query.filter(Task.project_id == project_id).all()
            task_list = get_task_list(tasks)
        return index(task_list=task_list)
    else:
        return jsonify({"error": "Method not allowed"}, 405)
