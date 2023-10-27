from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

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


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Boolean, default=True)
    phone = db.Column(db.String(100))
    email = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    create_uid = db.Column(db.Integer, default=0)
    write_uid = db.Column(db.Integer, default=0)
    role = db.Column(db.String(100))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    db.UniqueConstraint(username)

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
