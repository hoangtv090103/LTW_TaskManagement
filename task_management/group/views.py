from flask import render_template, redirect, url_for, flash, Blueprint
from flask_login import current_user

from task_management.group.forms import GroupForm

group_blueprint = Blueprint('groups', __name__, template_folder='templates', static_folder='static')
from task_management.forms import *
from task_management.models import *


@group_blueprint.route('/', methods=['GET', 'POST'])
def groups():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    groups = Group.query.all()
    return render_template('group_list.html', groups=groups, view_type='list')


@group_blueprint.route('/new', methods=['POST', 'GET'])
def new_group():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = GroupForm()
    if form.validate_on_submit():
        try:
            users = User.query.filter(User.id.in_(form.users.data)).all()
            group = Group(name=form.name.data, users=users)
            db.session.add(group)
            db.session.commit()
            return redirect(url_for('groups'))
        except Exception as e:
            print(e)
            db.session.rollback()
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a group: {err_msg}', category='danger')
    return render_template('group_new.html', form=form)


@group_blueprint.route('/<int:group_id>', methods=['POST', 'GET'])
def group_by_id(group_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    groups = db.get_or_404(Group, ident=group_id)
    return render_template('group_list.html', groups=groups, view_type='list')
