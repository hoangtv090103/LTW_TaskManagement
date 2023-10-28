from flask import redirect, url_for, render_template, flash
from flask_login import login_user, current_user, logout_user

from task_management import app
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
            return redirect(url_for('projects.projects'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/', methods=['POST', 'GET'])
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('base.html')


@app.route('/tasks')
def tasks():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    tasks = Task.query.all()
    return render_template('task.html', tasks=tasks)


@app.route('/settings')
def settings():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('settings.html')
