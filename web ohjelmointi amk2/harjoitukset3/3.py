import copy

from flask import Flask, request, jsonify, make_response, render_template

app = Flask(__name__)

students = [
{"student_number": 123123,
"name": "Alice Brown",
"credits": 130,
"degree": "it"},
{"student_number": 111222,
"name": "Bob Jones",
"credits": 157,
"degree": "it"},
{"student_number": 333444,
"name": "Richard Brown",
"credits": 57,
"degree": "it"}
]

@app.route("/home")
def homePage():
    return render_template("home.html",students=students)

@app.route("/modify/<name>")
def modifyPage(name):
    for student in students:
        print(name)
        print(student)
        if name == student["name"]:
            return render_template("modify.html",student=student)
    else:
        return render_template("error.html")

@app.route("/modified",methods=["POST"])
def modifiedPage():
    name = request.form["modifyName"]
    degree = request.form["modifyDegree"]
    credits = request.form["modifyCredits"]
    for (index,student) in enumerate(students):
        if name == student["name"]:
            student["degree"] = degree
            student["credits"] = credits
           # students[index] = student
    return render_template("home.html",students=students)


@app.route("/add")
def addingPage():
    return render_template("add.html")


@app.route("/added",methods=["POST"])
def addingMethod():
    number = request.form["addNumber"]
    name = request.form["addName"]
    degree = request.form["addDegree"]
    credits = request.form["addCredits"]
    message = "Student already in list."
    for student in students:
        print(student["student_number"])
        if name == student["name"]:
            return render_template("home.html", students=students,message=message)
    else:
        new_student = {
            "student_number": number,
            "name": name,
            "degree": degree,
            "credits": credits
            }
        new_student_copy = new_student.copy()
        students.append(new_student_copy)
        return render_template("home.html",students=students)

@app.route("/delete/<name>")
def deleteStudent(name):
    print(name)
    for student in students:
        if name == student["name"]:
            students.remove(student)
            return render_template("home.html",students=students)
    else:
        return render_template("home.html", students=students)


if __name__=="__main__":
    app.run(debug=True)