from flask import *
from flask_mongoengine import MongoEngine
db = MongoEngine()

class students(db.Document):
    student_number = db.IntField()
    name = db.StringField()
    credits = db.IntField()
    degree = db.StringField()

student_bp = Blueprint('student_bp', __name__,template_folder='templates',static_folder="static")

@student_bp.route("/home",methods=["POST","GET"])
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



@student_bp.route("/modify/<name>")
def modifyPage(name):
    for student in students.objects:
        print(name)
        print(student)
        if name == student["name"]:
            return render_template("modify.html",student=student)
    else:
        return render_template("error.html")


@student_bp.route("/modified",methods=["POST"])
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


@student_bp.route("/add")
def addingPage():
    return render_template("add.html")


@student_bp.route("/added",methods=["POST"])
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


@student_bp.route("/delete/<name>")
def deleteStudent(name):
    print(name)
    for student in students.objects:
        if name == student["name"]:
            students.delete(student)
            return redirect("/home")
    else:
        return redirect("/home")


@student_bp.route("/postmantesting",methods=["POST"])
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


@student_bp.route("/postmantesting", methods=["GET"])
def gettingMethod():
    return make_response(jsonify(students.objects))
