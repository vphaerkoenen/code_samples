from flask import Flask,request,jsonify,make_response,redirect,render_template


app = Flask(__name__)

allstudents =[
    {
        "student_number":123123,
        "name":"Alice Brown",
        "credits":130,
        "degree":"it"
    },
    {
        "student_number":111222,
        "name":"Bob Jones",
        "credits":157,
        "degree":"it"
    },
    {
        "student_number":333444,
        "name":"Richard Brown",
        "credits":57,
        "degree":"machine"
    }
]


@app.route("/students/<snumber>",methods=["PUT"])
def putData(snumber):
    data = request.get_json()
    data["student_number"] = snumber
    for x in allstudents:
        if data["student_number"] == x["student_number"]:
            allstudents.remove(x)
            allstudents.append(data)
            for i in allstudents:#tämä on tapahtumien
                print(i)#tutkimista varten
            return make_response(jsonify("message:","student replaced"),200)

    allstudents.append(data)
    for j in allstudents:#tämä on tapahtumien
        print(j)#tutkimista varten
    return make_response(jsonify("message:","collection created"),201)


@app.route("/students/<snumber>",methods=["PATCH"])
def patchData(snumber):
    data = request.get_json()
    data["student_number"] = snumber
    for x in allstudents:
        if data["student_number"] == x["student_number"]:
            if ("name") in data:
                x["name"] = data["name"]
            if ("credits") in data:
                x["credits"] = data["credits"]
            if ("degree") in data:
                x["degree"] = data["degree"]
            for i in allstudents:#tämä on tapahtumien
                print(i)#tutkimista varten
            return make_response(jsonify("message:","collection updated"),200)

    allstudents.append(data)
    for j in allstudents:#tämä on tapahtumien
        print(j)#tutkimista varten
    return make_response(jsonify("message:","collection created"),201)



@app.route("/students/<snumber>",methods=["DELETE"])
def deleteData(snumber):
    for x in allstudents:
       if x["student_number"] == int(snumber):
           allstudents.remove(x)
           return make_response(jsonify("message:", "student deleted"), 200)

    return make_response(jsonify("message:","collection not found"),201)


@app.route("/")
def getHomePage():
    return render_template("index.html",allstudents=allstudents)



@app.route("/add")
def showForm():
    return render_template("addStudentForm.html")



@app.route("/testi")
def testiFunktio():
    return render_template("testi.html")


@app.route("/students",methods=["PATCH"])
def patchDataWithOutSnumber():
    data = request.get_json()
    for x in allstudents:
        if data["student_number"] == x["student_number"]:
            if ("name") in data:
                x["name"] = data["name"]
            if ("credits") in data:
                x["credits"] = data["credits"]
            if ("degree") in data:
                x["degree"] = data["degree"]
            for i in allstudents:  # tämä on tapahtumien
                print(i)  # tutkimista varten
            return make_response(jsonify("message:", "collection updated"), 200)

    allstudents.append(data)
    for j in allstudents:  # tämä on tapahtumien
        print(j)  # tutkimista varten
    return make_response(jsonify("message:", "collection created"), 201)


if __name__=="__main__":
    app.run(debug=True)