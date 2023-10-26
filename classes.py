# create table projects
# (
#     id          integer      not null PRIMARY KEY AUTOINCREMENT,
#     name        varchar(255) not null,
#     description text,
#     active      bool     default true,
#     sequence    integer,
#     user_id     integer      not null,
#     date_start  date,
#     date_end    date,
#     created_at  datetime default CURRENT_TIMESTAMP,
#     updated_at  datetime default CURRENT_TIMESTAMP,
#     create_uid  integer  default 1,
#     write_uid   integer  default 1,
#     foreign key (user_id) references users (id)
# );
import sqlite3

sqldbname = 'db/task_managament.db'


class Project:
    def __init__(self, id, name, description, active, sequence, user_id, date_start, date_end, create_uid, write_uid):
        self.id = id
        self.name = name
        self.description = description
        self.active = active
        self.sequence = sequence
        self.user_id = user_id
        self.date_start = date_start
        self.date_end = date_end
        self.create_uid = create_uid
        self.write_uid = write_uid

    def create(self):
        conn = sqlite3.connect(sqldbname)
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO projects (name, description, active, sequence, user_id, date_start, date_end, create_uid, write_uid) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (self['name'], self['description'], self['active'], self['sequence'], self['user_id'], self['date_start'],
             self['date_end'], self['create_uid'], self['write_uid']))
        conn.commit()
        conn.close()


class Task:
    # id          integer      not null PRIMARY KEY AUTOINCREMENT,
    # project_id  integer      not null,
    # name        varchar(255) not null,
    # description text,
    # active      bool     default true,
    # priority    integer,
    # sequence    integer,
    # date_start  date,
    # date_end    date,
    # created_at  datetime default CURRENT_TIMESTAMP,
    # updated_at  datetime default CURRENT_TIMESTAMP,
    # create_uid  integer  default 1,
    # write_uid   integer  default 1,
    # tag_id      integer,
    def __init__(self, id, project_id, name, description, active, priority, sequence, date_start, date_end, create_uid,
                 write_uid, tag_id):
        self.id = id
        self.project_id = project_id
        self.name = name
        self.description = description
        self.active = active
        self.priority = priority
        self.sequence = sequence
        self.date_start = date_start
        self.date_end = date_end
        self.create_uid = create_uid
        self.write_uid = write_uid
        self.tag_id = tag_id
