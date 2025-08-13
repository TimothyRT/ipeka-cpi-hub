# Flask modules
from flask import Blueprint, render_template


core_bp = Blueprint("core", __name__, url_prefix="/")


@core_bp.route("/")
def home_route():
    return render_template("pages/home.html")


@core_bp.route("/staff", defaults={"grade": "ro"}, strict_slashes=False)
@core_bp.route("/staff/<grade>")
def staff_route(grade: str):
    grade = grade.lower()
    grade_ext = ""
    match grade:
        case "kg":
            grade_ext = "Kindergarten Teacher"
        case "el":
            grade_ext = "Elementary Teacher"
        case "jh":
            grade_ext = "Junior High Teacher"
        case "sh":
            grade_ext = "Senior High Teacher"
        case _:
            grade_ext = "Relation Office Staff"
    return render_template("pages/staff.html", grade=grade, grade_ext=grade_ext)


@core_bp.route("/test")
def test_route():
    return render_template("pages/test.html")


@core_bp.route("/test_admin")
def test_admin_route():
    return render_template("pages/test_admin.html")


@core_bp.route("/magolor")
def magolor():
    return render_template("pages/magolor.html")