import os
from flask import Flask, render_template
from models.Database import db
from routes.student_bp import student_bp
from routes.auth import auth
from flask_login import LoginManager, login_required, current_user
from models.User import User

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'users',
    'host': 'localhost',
    'port': 27017
}
app.config['SECRET_KEY'] = os.urandom(32)
db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

app.register_blueprint(student_bp, url_prefix='/students')
app.register_blueprint(auth, url_prefix="/auth")

@app.route('/')
def index():
    print("index function called")
    return render_template('index.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.objects.get(id = user_id)

if __name__ == '__main__':
    app.debug = True
    app.run()
