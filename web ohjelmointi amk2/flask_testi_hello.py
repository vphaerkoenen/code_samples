from flask import Flask
app = Flask(__name__)

@app.route("/")
def showHello():
    return "Hello"

@app.route("/users/<name>")
def showUsers(name):
   # allUsers = {"nimi":"Jack","osoite":"USA"}
    return "User"+name+"was found"

@app.route("/blog/<int:postId>")
def show_blog(postId):
    return "Blog number %d"%postId




if __name__=="__main__":
    app.run(debug=True)