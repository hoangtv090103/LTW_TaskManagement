from flask import request, session, redirect, url_for, render_template

from task_management import app, db
from task_management.models import *


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.one_or_404(db.select(User).filter_by(username=username, password=password),
                             description="Invalid username or password")
        if user:
            session['username'] = request.form['username']
            return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/', methods=['POST', 'GET'])
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/groups', methods=['GET', 'POST'])
def groups():
    if 'username' not in session:
        return redirect(url_for('login'))
    groups = Group.query.all()
    return render_template('group_list.html', groups=groups)


@app.route('/groups/new', methods=['POST', 'GET'])
def new_group():
    if 'username' not in session:
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
    if 'username' not in session:
        return redirect(url_for('login'))
    groups = db.get_or_404(Group, ident=group_id)
    return render_template('group_list.html', group=group)


@app.route('/users', methods=['POST', 'GET'])
def users():
    if 'username' not in session:
        return redirect(url_for('login'))
    users = User.query.all()
    return render_template('user_list.html', users=users)


@app.route('/users/new', methods=['POST', 'GET'])
def new_user():
    if 'username' not in session:
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
    if 'username' not in session:
        return redirect(url_for('login'))
    user = db.get_or_404(User, ident=user_id)
    return render_template('user_list.html', user=user)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/projects', methods=['POST', 'GET'])
def projects():
    if 'username' not in session:
        return redirect(url_for('login'))
    projects = Project.query.all()
    return render_template('project_list.html', projects=projects)


@app.route('/project/<int:id>', methods=['POST', 'GET'])
def project_by_id(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    project = db.get_or_404(Project, ident=id)
    return render_template('project_list.html', project=project)


@app.route('/tasks')
def tasks():
    if 'username' not in session:
        return redirect(url_for('login'))
    tasks = Task.query.all()
    return render_template('task.html', tasks=tasks)


@app.route('/settings')
def settings():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('settings.html')
