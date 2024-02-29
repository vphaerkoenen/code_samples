from flask import Blueprint
from controllers.StudentController import index, add_form, store, show, update, destroy
student_bp = Blueprint('student_bp', __name__)
student_bp.route('/', methods=['GET'])(index)
student_bp.route('/add', methods=['GET'])(add_form)
student_bp.route('/create', methods=['POST'])(store)
student_bp.route('/<int:student_id>', methods=['GET'])(show)
student_bp.route('/<int:student_id>/edit', methods=['POST'])(update)
student_bp.route('/<int:student_id>', methods=['DELETE'])(destroy)