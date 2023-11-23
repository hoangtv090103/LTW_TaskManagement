from flask import Blueprint
from flask import render_template, redirect, url_for, flash
from flask_login import current_user

from task_management.models import *
from task_management.user.forms import UserForm

user_blueprint = Blueprint('users', __name__, template_folder='templates', static_folder='static')


@user_blueprint.route('/', methods=['GET', 'POST'])
def users():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    users = User.query.all()
    return render_template('user_list.html', users=users, view_type='list')


@user_blueprint.route('/new', methods=['POST', 'GET'])
def new_user():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = UserForm()
    if form.validate_on_submit():
        try:
            user = User(name=form.name.data, username=form.username.data, password=form.password.data,
                        active=form.active.data, phone=form.phone.data, email=form.email.data,
                        is_admin=form.is_admin.data)
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


@user_blueprint.route('/<int:id>/edit', methods=['POST', 'GET'])
def edit_user(id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    user = db.get_or_404(User, ident=id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        try:
            user.name = form.name.data
            user.username = form.username.data
            user.password = form.password.data
            user.active = form.active.data
            user.phone = form.phone.data
            user.email = form.email.data
            db.session.commit()
            return redirect(url_for('users.users'))
        except Exception as e:
            print(e)
            db.session.rollback()
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('user_edit.html', form=form, user=user)


@user_blueprint.route('/<int:id>/delete', methods=['POST', 'GET'])
def delete_user(id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    user = db.get_or_404(User, ident=id)
    try:
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('users.users'))
    except Exception as e:
        print(e)
        db.session.rollback()
        return redirect(url_for('users.users'))

@user_blueprint.route('/profile', methods=['POST', 'GET'])
def get_profile(id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    user = db.get_or_404(User, ident=id)
    try:
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('users.users'))
    except Exception as e:
        print(e)
        db.session.rollback()
        return redirect(url_for('users.users'))

@user_blueprint.route('/<int:id>/change_password', methods=['POST', 'GET'])
def change_password(id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    user = db.get_or_404(User, ident=id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        try:
            user.password = form.password.data
            db.session.commit()
            return redirect(url_for('users.users'))
        except Exception as e:
            print(e)
            db.session.rollback()
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('user_change_password.html', form=form, user=user)
