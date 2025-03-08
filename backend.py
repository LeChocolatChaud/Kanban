from flask import Flask, request, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from jsonschema import validate
import database

app = Flask(__name__)

class User(UserMixin):
    def __init__(self, id, name, password, group):
        self.id = id
        self.name = name
        self.password = password
        self.group = group
    
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    possible_account = database.get_account(int(user_id))[0]
    if possible_account:
        return User(*possible_account)
    else:
        return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        ## Verify the username and password
        user = next((user for user in users.values() if user.username == username), None)
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('protected'))
        else:
            return 'Invalid username or password'

    return '''
        <form method="post">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required>
            <input type="submit" value="Login">
        </form>
    '''

@app.route('/api', methods=['GET'])
def api_root():
    return jsonify({'status': 'ok'})

@app.route('/api/projects', methods=['GET'])
def api_projects():
    return jsonify(database.get_projects())

@app.route('/api/project/<project_id>', methods=['GET'])
def api_project(project_id):
    return jsonify(database.get_project(project_id))

PROJECT_SCHEMA = {
    "type": "object",
    "properties": {
        name, description, creator_id
    }
}
@app.route('/api/project', methods=['POST'])
def api_create_project():
    data = request.get_json()
    

if __name__ == '__main__':
    app.run(debug=True)