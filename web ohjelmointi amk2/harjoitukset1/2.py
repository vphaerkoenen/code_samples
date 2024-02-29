from flask import Flask,request,make_response,redirect

app = Flask(__name__)

storage = []

@app.route("/handler",methods=["POST"])
def handler():
    if request.method=="POST":
        storage.clear()
        name = request.form["name"]

        if len(name) > 0:
            storage.append(str("'Nimi': '"+name+"'"))

        else:
            return redirect("fail")

        category = request.form["category"]
        storage.append(str("'Kategoria':'"+category+"'"))

        price = request.form["price"]
        if len(price) > 0:
            storage.append(str("'Hinta':'"+price+"'"))

        else:
            return redirect("fail")
        return redirect("success")

    else:
        return "Request method was not correct"

@app.route("/success",methods=["GET"])
def success():
    return make_response("Tuote {"+(" , ".join(storage)+"} lisätty"))

@app.route("/fail",methods=["GET"])
def fail():
    return "Tuotetta ei lisätty.Tuotteella täytyy olla nimi ja hinta."

@app.route("/application",methods=["GET"])
def application():
    return "<html>" \
            "<head>"\
            "<style>"\
                ".label:{font-size:18;}"\
            "</style>"\
            "</head>"\
              "<body>" \
                  "<form action = 'http://localhost:5000/handler' method='post'>" \
                    "<table>"\
                        "<tr>"\
                            "<td>"\
                                "<label >Tuotteen nimi:</label>" \
                                "<input Name='name' type='text' ></input>"\
                            "</td>"\
                        "</tr>"\
                        "<tr height=14></tr>"\
                        "<tr>"\
                            "<td>"\
                                '<label >Kategoria</label>'\
                                "<select Name='category' style='margin-left:10' >" \
                                    "<option value='juoma'>Juoma</option>" \
                                    "<option value='lihatuote'>Lihatuote</option>" \
                                    "<option value='hedelmät' >Hedelmät</option>"\
                                "</select>"\
                            "</td>"\
                        "</tr>"\
                        "<tr height=14></tr>"\
                        "<tr>"\
                            "<td>"\
                                "<label>Hinta</label>"\
                                "<input Name='price' style='margin-left:10'; ></input>"\
                            "</td>"\
                        "</tr>"\
                        "<tr height=14></tr>"\
                        "<tr>"\
                            "<td>"\
                                "<button Name='button'  >Submit</button>"\
                            "</td>"\
                        "</tr>"\
                    "</table>"\
                "</form>" \
           "</body>" \
           "</html>"

if __name__=="__main__":
    app.run(debug=True)