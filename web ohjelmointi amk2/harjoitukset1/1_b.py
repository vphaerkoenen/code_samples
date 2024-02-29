from flask import Flask,jsonify

app = Flask(__name__)

allstudents = [
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

@app.route("/students/<string:degree>",methods=["GET"])
def showAll(degree):
    storage=[]
    for i in allstudents:
        if ("it") in i.values():
           storage.append(i)
    return jsonify(storage)

if __name__=="__main__":
    app.run(debug=True)