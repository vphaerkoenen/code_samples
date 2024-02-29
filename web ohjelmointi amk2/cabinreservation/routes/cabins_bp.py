import os
import random
from datetime import datetime
import flask_login
import requests_file
from flask import *
from flask_mongoengine import MongoEngine
from werkzeug.security import generate_password_hash, check_password_hash
db = MongoEngine()
from flask_login import *

class users(db.Document):
    id_for_reserve = db.IntField()
    user_email = db.EmailField()
    password = db.StringField(max_length=100)
    fname = db.StringField()
    lname = db.StringField()
    reserved = db.StringField()
    startdate = db.DateTimeField()
    enddate = db.DateTimeField()

users_bp = Blueprint('users_bp', __name__,template_folder='templates',static_folder="static")

@users_bp.route('/login',methods=["GET","POST"])#jos halutaan poistaa varaus mennään tätä reittiä
def login():
    deletingid_for_reserve = int(request.form["id_for_reserve"])  # meinasi tökätä tähän,tietotyypit ei olleet samat ja poisto ei onnistunut
    deletinguser_email = request.form["user_email"]
    deletingpassword = request.form["password"]
    print(deletinguser_email)
    print(deletingid_for_reserve)
    print(deletingpassword)
    return render_template("/login.html",
                           deletingid_for_reserve=deletingid_for_reserve,#tietoja kuljetetaan mukana poistohetkeä varten (postlogininfo)
                           deletinguser_email=deletinguser_email,
                           deletingpassword=deletingpassword)

@users_bp.route('/postlogininfo',methods=["POST"])#tämä reitti tarkistaa varauksen poistajan kirjautumisen ja poistaa varauksen
def postlogininfo():
    email = request.form["email"]
    password = request.form["password"]
    deletinguser_email = request.form["deletinguser_email"]
    deletingid_for_reserve = int(request.form["deletingid_for_reserve"])
    deletingpassword = request.form["deletingpassword"]
    print(email)
    print(password)
    print(deletinguser_email)
    print(deletingid_for_reserve)
    print(deletingpassword)
    print("tarkistetaan kirjautumistiedot...")
    for i in users.objects:
        print(i["user_email"])
        print(i["password"])
        if email == i["user_email"]and password == i["password"]:
            print("sisäänkirjautuminen")
            for user in users.objects:
                if user["id_for_reserve"] == deletingid_for_reserve:  # poisto tapahtuu varauksessa luodun random-numeron avulla
                    print("poistetaan")
                    users.delete(user)
                    flash("Varaus poistettu!")
                    return redirect("/deletereservation")
    else:
        print("kirjautumistiedot ei käy")
        flash("Kirjautumistiedot ei vastanneet varauksen tietoja! Varausta ei poistettu!")
        return redirect("/deletereservation")

@users_bp.route("/home",methods=["POST","GET"])
def homePage():
    return render_template("cabinhome.html")

@users_bp.route("/contact")
def contact():
    return render_template("contact.html")

@users_bp.route("/kylmala")
def kylmala():
    return render_template("kylmala.html")

@users_bp.route("/rauhala")
def rauhala():
    return render_template("rauhala.html")

@users_bp.route("/sammalmaja")
def sammalmaja():
    return render_template("sammalmaja.html")

@users_bp.route("/takasyrja")
def takasyrja():
    return render_template("takasyrja.html")

@users_bp.route("/reserve",methods=["POST"])
def reserve():
    location = request.form.get("location")
    print(location)
    if users:
        return render_template("reserve.html", location=location,users=users.objects(reserved=location))
    else:
        return render_template("reserve.html", location=location)

@users_bp.route("/confirmation",methods=["POST"])#tämä reitti tallentaa varauksen
def confirmation():
    firstday = request.form["firstday"]
    lastday = request.form["lastday"]
    location = request.form["location"]
    email = request.form["email"]
    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    passwd = request.form["passwd"]
    id_for_reserve = random.randint(1,1000)
    print(firstday)
    print(lastday)
    print(location)
    print(email)
    print(firstname)
    print(lastname)
    print(passwd)
    print(id_for_reserve)
    new_user = users(
        id_for_reserve=id_for_reserve,
        user_email=email,
        fname=firstname,
        lname=lastname,
        reserved=location,
        startdate=firstday,
        enddate=lastday,
        password=passwd)
    new_user.save()
    return render_template("confirmation.html")

@users_bp.route("/reservations",methods=["GET","POST"])
def reservations():
    return render_template("reservations.html",users=users.objects.order_by("reserved"))

@users_bp.route("/deletereservation",methods=["GET","POST"])
def deletereservation():
    return render_template("deletereservation2.html", users=users.objects.order_by("reserved"))
