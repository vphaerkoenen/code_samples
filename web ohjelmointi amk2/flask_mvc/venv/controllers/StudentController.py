# pseudo code
import sys
from flask import render_template, redirect, url_for, request, abort, make_response, jsonify
from models.Student import Student
from flask_login import login_required

@login_required
def index():
    students = Student.objects
    return render_template("students.html", students=students)

@login_required
def add_form():
    return render_template("add_student.html")

@login_required
# Dummy implementation to add a student e.g. using postman
def store():
    form_data = request.form
    print(form_data)
    student = Student(studentid=form_data["student_number"], name=form_data["name"],
                      study_field=form_data["degree"], credits=form_data["credits"])
    student.save()
    students = Student.objects
    #return make_response(jsonify(student), 200)
    return render_template("students.html", students=students)

#Instead of returning text you should render the template in the following methods
# You also need to implement the templates and add the necessary links to base.html file
@login_required
def show(student_id):
    students = Student.objects(studentid=student_id)
    
    return make_response(jsonify(students), 200)

@login_required
def update(student_id):
    student = Student.objects(studentid=student_id).first()

    return make_response("update", 200)

@login_required
def delete(student_id):
    return make_response("delete", 200)

@login_required
def destroy(student_id):
    return make_response("destroy", 200)