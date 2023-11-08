from flask_login import UserMixin  # UserMixin là một class có sẵn trong flask_login để hỗ trợ việc quản lý user

from task_management import db, bcrypt, login_manager

group_user = db.Table('group_user',
                      db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True),
                      db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
                      )


class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    create_uid = db.Column(db.Integer, default=0)
    write_uid = db.Column(db.Integer, default=0)
    users = db.relationship('User', secondary=group_user, backref='groups')
    access_rights = db.relationship('AccessRight', backref='group')

    def __repr__(self):
        return '<Group %r>' % self.name


@login_manager.user_loader
def load_user(user_id):
    """
    Hàm này được sử dụng để load user từ session khi user đã đăng nhập
    :param user_id:
    :return:
    """
    return User.query.get(int(user_id))



class User(db.Model, UserMixin):
    """
    UserMixin là một class có sẵn trong flask_login để hỗ trợ việc quản lý user
    """
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(100), nullable=False)
    password_hashed = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Boolean, default=True)
    phone = db.Column(db.String(100))
    email = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    create_uid = db.Column(db.Integer, default=0)
    write_uid = db.Column(db.Integer, default=0)
    is_admin = db.Column(db.Boolean, default=False)
    db.UniqueConstraint(username, email)

    @property  # Decorator này dùng để tạo ra một thuộc tính giả
    def password(self):
        if self.password_hashed is not None:
            return None
        return self.password

    @password.setter
    def password(self, password):
        """
        Hàm này được sử dụng để mã hóa password
        :param password:
        :return:
        """
        self.password_hashed = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        """
        Hàm này được sử dụng để kiểm tra password đã được mã hóa có khớp với password người dùng nhập vào hay không
        :param attempted_password:
        :return:
        """
        return bcrypt.check_password_hash(self.password_hashed, attempted_password)

    def __repr__(self):
        return '<User %r>' % self.username


class AccessRight(db.Model):
    __tablename__ = 'access_right'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    model = db.Column(db.String(100))
    create_perm = db.Column(db.Boolean, default=False)
    write_perm = db.Column(db.Boolean, default=False)
    delete_perm = db.Column(db.Boolean, default=False)
    read_perm = db.Column(db.Boolean, default=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    create_uid = db.Column(db.Integer, default=0)
    write_uid = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<AccessRight %r>' % self.name


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    create_uid = db.Column(db.Integer, default=0)
    write_uid = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Tag %r>' % self.name


class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    status = db.Column(db.String(100))
    active = db.Column(db.Boolean, default=True)
    sequence = db.Column(db.Integer)
    manager_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_start = db.Column(db.Date)
    date_end = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    create_uid = db.Column(db.Integer, default=0)
    write_uid = db.Column(db.Integer, default=0)
    tasks = db.relationship('Task', backref='project')
    progress = db.Column(db.Float)

    def __repr__(self):
        return '<Project %r>' % self.name


task_tag = db.Table('task_tag',
                    db.Column('task_id', db.Integer, db.ForeignKey('task.id'), primary_key=True),
                    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
                    )

task_user = db.Table('task_user',
                     db.Column('task_id', db.Integer, db.ForeignKey('task.id'), primary_key=True),
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
                     )


class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    user_ids = db.relationship('User', secondary=task_user, backref='tasks')
    status = db.Column(db.String(100))
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    active = db.Column(db.Boolean, default=True)
    priority = db.Column(db.Integer)
    sequence = db.Column(db.Integer)
    date_start = db.Column(db.Date)
    date_end = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    create_uid = db.Column(db.Integer, default=0)
    write_uid = db.Column(db.Integer, default=0)
    tag_ids = db.relationship('Tag', secondary=task_tag, backref='tasks')

    def __repr__(self):
        return '<Task %r>' % self.name
