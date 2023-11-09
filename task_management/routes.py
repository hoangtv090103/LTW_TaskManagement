from flask import redirect, url_for, render_template, flash, session
from flask_login import login_user, current_user, logout_user

from task_management.forms import *
from task_management.models import *


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            username=form.username.data,
            password=form.password1.data,
            email=form.email.data, phone=form.phone.data)
        try:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        except Exception as e:
            print(e)
            db.session.rollback()  # Rollback the changes on error
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('register.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)  # Lệnh này sẽ lưu thông tin user vào session
            return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    projects = Project.query.filter(Project.manager_id == current_user.id).all()
    active_project = False
    active_task = False
    task_list = False
    create_uid = False
    mode = session.get('mode', '')
    keyword = session.get('keyword', '')

    if session.get('active_task_id'):
        active_task = Task.query.get(session.get('active_task_id'))
        create_uid = User.query.get(active_task.user_id)

    elif session.get('active_project_id'):
        session.pop('active_task_id', None)
        active_project = Project.query.get(session.get('active_project_id'))
        create_uid = User.query.get(active_project.manager_id)

        todo = Task.query.filter(Task.project_id == active_project.id, Task.status == 'todo')
        in_progress = Task.query.filter(Task.project_id == active_project.id, Task.status == 'in-progress')
        done = Task.query.filter(Task.project_id == active_project.id, Task.status == 'done')

        if keyword:
            keyword = keyword.strip().lower()
            todo = todo.filter(Task.name.like(f'%{keyword}%'))
            in_progress = in_progress.filter(Task.name.like(f'%{keyword}%'))
            done = done.filter(Task.name.like(f'%{keyword}%'))

        todo = todo.all()
        in_progress = in_progress.all()
        done = done.all()

        todo.sort(key=lambda x: x.priority, reverse=True)
        in_progress.sort(key=lambda x: x.priority, reverse=True)
        done.sort(key=lambda x: x.priority, reverse=True)

        task_list = {'todo': todo,
                     'in-progress': in_progress,
                     'done': done}
    session.pop('keyword', None)

    return render_template('index.html',
                           projects=projects,
                           active_project=active_project,
                           active_task=active_task,
                           create_uid=create_uid,
                           mode=mode,
                           task_list=task_list)


@app.route('/settings')
def settings():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('settings.html')
