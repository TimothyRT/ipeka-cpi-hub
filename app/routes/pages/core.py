# Flask modules
from flask import Blueprint, redirect, render_template, url_for


core_bp = Blueprint("core", __name__, url_prefix="/")


@core_bp.route("/")
def home_route():
    return render_template("pages/home.html")


@core_bp.route("/staff", strict_slashes=False)
def staff_route_generic():
    landing_route_kg = url_for("pages.core.staff_route", grade="kg")
    landing_route_el = url_for("pages.core.staff_route", grade="el")
    landing_route_jh = url_for("pages.core.staff_route", grade="jh")
    landing_route_sh = url_for("pages.core.staff_route", grade="sh")
    landing_route_ro = url_for("pages.core.staff_route", grade="ro")
    return render_template(
        "pages/landing.html",
        type="Staff/teacher List",
        landing_route_kg=landing_route_kg,
        landing_route_el=landing_route_el,
        landing_route_jh=landing_route_jh,
        landing_route_sh=landing_route_sh,
        landing_route_ro=landing_route_ro
    )


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