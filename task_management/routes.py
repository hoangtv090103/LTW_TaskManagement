from flask import request, redirect, url_for, render_template, flash
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
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('projects'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for('login'))


@app.route('/', methods=['POST', 'GET'])
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('base.html')


@app.route('/groups', methods=['GET', 'POST'])
def groups():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    groups = Group.query.all()
    return render_template('group_list.html', groups=groups)


@app.route('/groups/new', methods=['POST', 'GET'])
def new_group():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        group = Group(name=name)
        for user_id in request.form.getlist('users'):
            user = db.one_or_404(db.select(User).filter_by(id=user_id))
            group.users.append(user)
        db.session.add(group)
        db.session.commit()
        return redirect(url_for('groups'))
    return render_template('group_new.html')


@app.route('/groups/<int:group_id>', methods=['POST', 'GET'])
def group_by_id(group_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    groups = db.get_or_404(Group, ident=group_id)
    return render_template('group_list.html', groups=groups)


@app.route('/users', methods=['POST', 'GET'])
def users():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    users = User.query.all()
    return render_template('user_list.html', users=users)


@app.route('/users/new', methods=['POST', 'GET'])
def new_user():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        phone = request.form['phone']
        email = request.form['email']
        role = request.form['role']
        user = User(name=name, username=username, password=password, phone=phone, email=email, role=role)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('users'))
    return render_template('user_new.html')


@app.route('/users/<int:user_id>', methods=['POST', 'GET'])
def user_by_id(user_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    user = db.get_or_404(User, ident=user_id)
    return render_template('user_list.html', user=user)


@app.route('/projects', methods=['POST', 'GET'])
def projects():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    projects = Project.query.all()
    return render_template('project_list.html', projects=projects)

@app.route('/projects/new', methods=['POST', 'GET'])
def new_project():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(name=form.name.data, description=form.description.data, sequence=form.sequence.data,
                          manager_id=form.manager_id.data)
        db.session.add(project)
        db.session.commit()
        return redirect(url_for('projects'))
    return render_template('project_new.html', form=form)

@app.route('/project/<int:id>', methods=['POST', 'GET'])
def project_by_id(id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    project = db.get_or_404(Project, ident=id)
    return render_template('project_list.html', project=project)


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
