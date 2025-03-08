from collections import namedtuple
import sqlite3

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        self.cursor.execute(query)
        self.conn.commit()

    def insert_data(self, table_name, data): 
        query = f"INSERT INTO {table_name} VALUES ({','.join(['?' for _ in data])})"
        self.cursor.execute(query, data)
        self.conn.commit()

    def select_data(self, table_name, columns='*', condition=None):
        query = f"SELECT {columns} FROM {table_name}"
        if condition:
            query += f" WHERE {condition}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def update_data(self, table_name, set_clause, condition):
        query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
        self.cursor.execute(query)
        self.conn.commit()

    def delete_data(self, table_name, condition):
        query = f"DELETE FROM {table_name} WHERE {condition}"
        self.cursor.execute(query)
        self.conn.commit()

    def close_connection(self):
        self.cursor.close()
        self.conn.close()
        print("Database connection closed")

    def __del__(self):
        self.close_connection()


db = Database('data.db')

db.create_table('users', 'id INTEGER UNIQUE, name TEXT, password TEXT, group TEXT')
UserTuple: type = namedtuple('UserTuple', 'id name password group')

db.create_table('projects', 'id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, description TEXT, creator_id INTEGER, admins TEXT, FOREIGN KEY(creator_id) REFERENCES users(id)')
ProjectTuple: type = namedtuple('ProjectTuple', 'id name description creator_id admins')

db.create_table('tasks', 'id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, description TEXT, status TEXT, creation_date INTEGER, due_date INTEGER, project_id INTEGER, assignee_id INTEGER, involved_users TEXT, FOREIGN KEY(project_id) REFERENCES projects(id), FOREIGN KEY(assignee_id) REFERENCES users(id)')
TaskTuple: type = namedtuple('TaskTuple', 'id name description status creation_date due_date project_id assignee_id involved_users')

db.create_table('comments', 'id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT, task_id INTEGER, user_id INTEGER, creation_date INTEGER, FOREIGN KEY(task_id) REFERENCES tasks(id), FOREIGN KEY(user_id) REFERENCES users(id)')
CommentTuple: type = namedtuple('CommentTuple', 'id content task_id user_id creation_date')

def add_account(id, name, password, group):
    db.insert_data('users', (id, name, password, group))

def add_project(name, description, creator_id):
    db.insert_data('projects', (name, description, creator_id))

def add_task(name, description, status, creation_date, due_date, project_id, assignee_id, involved_users):
    db.insert_data('tasks', (name, description, status, creation_date, due_date, project_id, assignee_id, involved_users))

def add_comment(content, task_id, user_id, creation_date):
    db.insert_data('comments', (content, task_id, user_id, creation_date))

def delete_account(id):
    db.delete_data('users', f"id={id}")

def delete_project(id):
    db.delete_data('projects', f"id={id}")

def delete_task(id):
    db.delete_data('tasks', f"id={id}")

def delete_comment(id):
    db.delete_data('comments', f"id={id}")

def get_accounts() -> list[UserTuple]:
    return db.select_data('users')

def get_account(id) -> list[UserTuple]:
    return db.select_data('users', f"id={id}")

def validate_account(id, password):
    selected = db.select_data('users', f"id={id} AND password='{password}'")
    if len(selected) > 0:
        return True
    else:
        return False

def get_projects():
    return db.select_data('projects')

def get_project(id):
    return db.select_data('projects', f"id={id}")

def get_user_projects(user_id):
    return db.select_data('projects', f"creator_id={user_id}")

def get_project_tasks(project_id):
    return db.select_data('tasks', f"project_id={project_id}")

def get_user_tasks(user_id):
    return db.select_data('tasks', f"assignee_id={user_id}")

def get_user_involved_tasks(user_id):
    return db.select_data('tasks', f"involved_users LIKE '%{user_id},%'")

def get_task(id):
    return db.select_data('tasks', f"id={id}")

def get_task_comments(task_id):
    return db.select_data('comments', f"task_id={task_id}")

def get_user_comments(user_id):
    return db.select_data('comments', f"user_id={user_id}")

def get_comment(id):
    return db.select_data('comments', f"id={id}")

def update_account(id, name, password, group):
    db.update_data('users', f"id={id}", (name, password, group))

def update_project(id, name, description, creator_id):
    db.update_data('projects', f"id={id}", (name, description, creator_id))

def update_task(id, name, description, status, creation_date, due_date, project_id, assignee_id, involved_users):
    db.update_data('tasks', f"id={id}", (name, description, status, creation_date, due_date, project_id, assignee_id, involved_users))

def update_comment(id, content, task_id, user_id, creation_date):
    db.update_data('comments', f"id={id}", (content, task_id, user_id, creation_date))