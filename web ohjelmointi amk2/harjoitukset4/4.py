import copy
from flask import Flask, request, jsonify, make_response, render_template,redirect
from flask_mongoengine import *


app = Flask(__name__)
db = MongoEngine()
db.init_app(app)


app.config['MONGODB_SETTINGS'] = {
    'db':'webharjoitus4',
    'host':'localhost',
    'port':27017
}


class students(db.Document):
    student_number = db.IntField()
    name = db.StringField()
    credits = db.IntField()
    degree = db.StringField()



@app.route("/home",methods=["POST","GET"])
def homePage():
    if request.method == "POST":
        degree = request.form.get("homeDegree")
        if degree == "kaikki":
            return render_template("home.html", students=students.objects.order_by('student_number'))
        if degree == "it":
            return render_template("home.html",students=students.objects(degree="it").order_by('student_number'))
        if degree == "art":
            return render_template("home.html",students=students.objects(degree="art").order_by('student_number'))
    else:
        return render_template("home.html", students=students.objects.order_by('student_number'))



@app.route("/modify/<name>")
def modifyPage(name):
    for student in students.objects:
        print(name)
        print(student)
        if name == student["name"]:
            return render_template("modify.html",student=student)
    else:
        return render_template("error.html")


@app.route("/modified",methods=["POST"])
def modifiedPage():
    number = request.form["modifyNumber"]
    name = request.form["modifyName"]
    degree = request.form["modifyDegree"]
    credits = request.form["modifyCredits"]
    for student in students.objects:
        if name == student["name"]:
            student.update(
                student_number=number,
                name=name,
                degree=degree,
                credits=credits
                )
    return redirect("/home")


@app.route("/add")
def addingPage():
    return render_template("add.html")


@app.route("/added",methods=["POST"])
def addingMethod():
    number = request.form["addNumber"]
    name = request.form["addName"]
    degree = request.form["addDegree"]
    credits = request.form["addCredits"]
    print(number)
    for student in students.objects:
        print(student["student_number"])
        if name == student["name"]:
            return redirect("/home")
    else:
        new_student = students(
            student_number=number,
            name=name,
            degree=degree,
            credits=credits
        )
        new_student.save()
        return redirect("/home")


@app.route("/delete/<name>")
def deleteStudent(name):
    print(name)
    for student in students.objects:
        if name == student["name"]:
            students.delete(student)
            return redirect("/home")
    else:
        return redirect("/home")


@app.route("/postmantesting",methods=["POST"])
def methodAdding():
    data = request.get_json()
    print(data)
    for student in students.objects:
        #print(student["student_number"])
        if data["name"] == student["name"]:
            return make_response(jsonify("data on jo listassa"))
    else:
        new_student = students(
            student_number=data["student_number"],
            name=data["name"],
            degree=data["degree"],
            credits=data["credits"]
            )
        new_student.save()
        return make_response(jsonify("new_student:lisätty"))


@app.route("/postmantesting", methods=["GET"])
def gettingMethod():
    return make_response(jsonify(students.objects))

if __name__=="__main__":
    app.run(debug=True)