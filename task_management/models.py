from datetime import timedelta, date

from flask_login import UserMixin  # UserMixin là một class có sẵn trong flask_login để hỗ trợ việc quản lý user
from flask_mail import Message

from task_management import db, bcrypt, login_manager, mail, scheduler, app


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


class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
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

    def __repr__(self):
        return '<Task %r>' % self.name


def reminder():
    with app.app_context():
        tasks = Task.query.filter_by(date_end=date.today() + timedelta(days=1)).all()
        for task in tasks:
            user = User.query.get(task.user_id)
            message = Message(
                subject=f'Task reminder from Task Management',
                recipients=[user.email],
                sender='tranh459789@gmail.com'
            )
            message.body = f'Hello {user.name},\n You have a task to complete: {task.name}\nDue date: {task.date_end}'
            mail.send(message)


# convert to local time
scheduler.add_job(id='Scheduled task', func=reminder, trigger='cron', hour=0, minute=0, second=0, day_of_week='mon-sun',
                  timezone='Asia/Ho_Chi_Minh')
scheduler.start()
