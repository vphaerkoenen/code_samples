from models.Database import db

class Student(db.Document):
    __tablename__ = 'students'
    studentid = db.IntField(required=True)
    name = db.StringField(max_length=50)
    study_field = db.StringField(max_length=50)
    credits = db.IntField()

    def _init__(self, id, name, field, credits):
        self.studentid = id,
        self.name = name,
        self.study_field = field
        self.credits = credits