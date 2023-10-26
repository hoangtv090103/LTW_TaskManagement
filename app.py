import os
import sqlite3

from flask import Flask, render_template, session, request, redirect, url_for

from classes import Project

app = Flask(__name__)
sqldbname = 'db/task_managament.db'

app.secret_key = os.urandom(24)


def get_database():
    conn = sqlite3.connect(sqldbname)
    return conn


def get_data_from_db(table_name=None, query=None, fetchone=False):
    if not table_name:
        return []
    conn = get_database()
    c = conn.cursor()
    if query:
        c.execute(query)
    else:
        c.execute("SELECT * FROM " + table_name)
    if fetchone:
        rows = c.fetchone()
    else:
        rows = c.fetchall()
    conn.close()
    return rows


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = get_data_from_db('users',
                                    "SELECT * FROM users WHERE login = '" +
                                    request.form['username'] + "' AND password = '" + request.form['password'] + "'",
                                    fetchone=True)
        if username:
            session['username'] = request.form['username']
            return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/', methods=['POST', 'GET'])
def index():  # put application's code here
    # if 'username' not in session:
    #     return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/projects')
def projects():
    #     id         integer      not null PRIMARY KEY AUTOINCREMENT,
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
    data = get_data_from_db('project')
    project_objs = []
    # Convert data to objects
    for row in data:
        project_objs.append(Project(row[0], row[1], row[2], row[3], row[4], row[5], row[6],
                                    row[7], row[8], row[9]))
    return render_template('projects.html', projects=project_objs)


@app.route('/tasks')
def tasks():
    return render_template('tasks.html')


if __name__ == '__main__':
    app.run(debug=True)
