from flask import Flask
#from flask_migrate import Migrate
from harjoitukset5.routes.student_bp import *
from flask_mongoengine import MongoEngine

db = MongoEngine()
app = Flask(__name__)
db.init_app(app)
app.config.from_pyfile("config.py")

app.register_blueprint(student_bp)

if __name__ == '__main__':
    app.debug = True
    app.run()