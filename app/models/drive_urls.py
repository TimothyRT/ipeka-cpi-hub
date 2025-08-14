from app.extensions import db
# from app.utils.models import generate_uuid
    
    
class AcademicCalendar(db.Model):
    __tablename__ = "academic_calendar"
    grade = db.Column(db.String, primary_key=True, unique=True, nullable=False)
    url = db.Column(db.String(255), nullable=True)
    
    def to_dict(self):
        return {"grade": self.grade, "url": self.url}
    
    
class ImportantFiles(db.Model):
    __tablename__ = "important_files"
    grade = db.Column(db.String, primary_key=True, unique=True, nullable=False)
    url = db.Column(db.String(255), nullable=True)
    
    def to_dict(self):
        return {"grade": self.grade, "url": self.url}
    
    
class StaffList(db.Model):
    __tablename__ = "staff_list"
    grade = db.Column(db.String, primary_key=True, unique=True, nullable=False)
    url = db.Column(db.String(255), nullable=True)
    
    def to_dict(self):
        return {"grade": self.grade, "url": self.url}


class TermOverview(db.Model):
    __tablename__ = "term_overview"
    grade = db.Column(db.String, primary_key=True, unique=True, nullable=False)
    url = db.Column(db.String(255), nullable=True)
    
    def to_dict(self):
        return {"grade": self.grade, "url": self.url}


class Timetable(db.Model):
    __tablename__ = "timetable"
    grade = db.Column(db.String, primary_key=True, unique=True, nullable=False)
    url = db.Column(db.String(255), nullable=True)
    
    def to_dict(self):
        return {"grade": self.grade, "url": self.url}
