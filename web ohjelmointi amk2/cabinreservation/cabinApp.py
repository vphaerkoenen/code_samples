import os
from flask_mongoengine import MongoEngine
from cabinreservation.routes.cabins_bp import *

db = MongoEngine()
MONGODB_SETTINGS = {
    'db':'cabinreservation',
    'host':'localhost',
    'port':27017
}
app = Flask(__name__)
db.init_app(app)
app.config['SECRET_KEY'] = os.urandom(32)
app.register_blueprint(users_bp)

if __name__ == '__main__':
    app.debug = True
    app.run()