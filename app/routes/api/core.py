from flask import Blueprint, current_app, jsonify, request

import os
import threading

from app.extensions import db
from app.models import Employee, AcademicCalendar, ImportantFiles, StaffList, TermOverview, Timetable
from app.utils.api import success_response
from utilities.downloader import download_drive_folder


core_api_bp = Blueprint("core_api", __name__, url_prefix="/")


@core_api_bp.route("/temuera", strict_slashes=False)
def temuera_morrison():
    return jsonify({
        "temuera": "morrison",
        "ENV": current_app.config["ENV"],
        "FLASK_DEBUG": str(os.environ.get("FLASK_DEBUG")),
        "SECRET_KEY": os.environ.get("SECRET_KEY")
    })


@core_api_bp.route("/staff", defaults={"grade": None}, strict_slashes=False)
@core_api_bp.route("/staff/<grade>", strict_slashes=False)
def get_staff(grade: None | str):
    if grade is None:
        rows = Employee.query.all()
    else:
        rows = Employee.query.filter_by(grade=grade.upper()).all()
    return jsonify([row.to_dict() for row in rows])


@core_api_bp.route("/drive/<cat>", defaults={"grade": None}, strict_slashes=False)
@core_api_bp.route("/drive/<cat>/<grade>", strict_slashes=False)
def get_drive_url(cat: None | str, grade: None | str):
    match cat:
        case "important-files":
            cat_class = ImportantFiles
        case "calendar":
            cat_class = AcademicCalendar
        case "term-overview":
            cat_class = TermOverview
        case "timetable":
            cat_class = Timetable
        case _:
            cat_class = StaffList
            
    if grade is None:
        rows = cat_class.query.all()
    else:
        rows = cat_class.query.filter_by(grade=grade.upper()).all()
    return jsonify([row.to_dict() for row in rows])
    

@core_api_bp.route("/drive", methods=["POST"], strict_slashes=False)
def edit_drive_url():
    data = request.get_json()
    cat = data.get('cat').lower()
    grade = data.get('grade').upper()
    value = data.get('value')

    match cat:
        case "important-files":
            cat_class = ImportantFiles
        case "calendar":
            cat_class = AcademicCalendar
        case "term-overview":
            cat_class = TermOverview
        case "timetable":
            cat_class = Timetable
        case _:
            cat_class = StaffList
    row = cat_class.query.filter_by(grade=grade).one_or_404()
    row.url = value
    db.session.commit()
    return success_response(message="Data successfully updated!")


def commit_processing_task(link, directory, delete_old_files=True):    
    print("Starting background task with:", link)
    
    if delete_old_files:
        download_drive_folder(
            link=link,
            directory=directory
        )
    
    print("Finished task")


@core_api_bp.route('/images', methods=['POST'])
def process_images():
    data = request.get_json()
    link: str = data["link"]
    directory: str = data["directory"]
    print(f"{link = }; {directory = }")
    threading.Thread(target=commit_processing_task, args=(link, directory)).start()
    return jsonify({'message': 'Image downloading & processing task has started in the background!'})
