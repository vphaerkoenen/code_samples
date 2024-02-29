from flask import Blueprint
from controllers.AuthController import login, signup, logout, signup_post, login_post
auth = Blueprint('auth', __name__)

auth.route('/login', methods=['GET'])(login)
auth.route('/signup')(signup)
auth.route('/logout')(logout)
auth.route('/signup', methods=['POST'])(signup_post)
auth.route('/login', methods=['POST'])(login_post)
