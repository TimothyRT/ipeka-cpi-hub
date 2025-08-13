from flask import Blueprint, jsonify, request

import threading

from app.models import Employee
from utilities.downloader import download_drive_folder


core_api_bp = Blueprint("core_api", __name__, url_prefix="/")


@core_api_bp.route("/staff/", defaults={"grade": None}, strict_slashes=False)
@core_api_bp.route("/staff/<grade>", methods=["GET"])
def get_staff(grade: None | str):
    if grade is None:
        staff = Employee.query.all()
    else:
        staff = Employee.query.filter_by(grade=grade.upper())
    return jsonify([s.to_dict() for s in staff])


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
