from app.extensions import db
# from app.utils.models import generate_uuid


class Employee(db.Model):
    index = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    nip = db.Column(db.String(10), nullable=True)
    grade = db.Column(db.String(3), nullable=True)
    position = db.Column(db.String(20), nullable=True)
    join_date = db.Column(db.String(20), nullable=True)
    date_of_birth = db.Column(db.String(20), nullable=True)
    gender = db.Column(db.String(1), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(40), nullable=True)
    
    def to_dict(self):
        return {"index": self.index, "name": self.name, "grade": self.grade, "position": self.position, "gender": self.gender}
