from flask import Blueprint
from flask import render_template, redirect, url_for, flash
from flask_login import current_user

from task_management.forms import UserForm
from task_management.models import *

user_blueprint = Blueprint('users', __name__, template_folder='templates', static_folder='static')


@user_blueprint.route('/', methods=['GET', 'POST'])
def users():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    users = User.query.all()
    return render_template('user_list.html', users=users)


@user_blueprint.route('/new', methods=['POST', 'GET'])
def new_user():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = UserForm()
    if form.validate_on_submit():
        try:
            user = User(name=form.name.data, username=form.username.data, password=form.password.data,
                        active=form.active.data, phone=form.phone.data, email=form.email.data, role=form.role.data,
                        group_id=form.group_id.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('users.users'))
        except Exception as e:
            print(e)
            db.session.rollback()
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('user_new.html', form=form)


@user_blueprint.route('/<int:user_id>', methods=['POST', 'GET'])
def user_by_id(user_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    user = db.get_or_404(User, ident=user_id)
    return render_template('user_detail.html', user=user)
