# Flask modules
from flask import Blueprint, render_template, url_for, redirect, session
from flask_dance.contrib.google import google

from app.models.drive_urls import AcademicCalendar, ImportantFiles, TermOverview, Timetable
from app.routes.google_oauth import require_oauth


core_bp = Blueprint("core", __name__, url_prefix="/")


@core_bp.route("/login_user")
def login_user():
    return render_template("oauth/login.html")


@core_bp.route("/")
@require_oauth()
def home_route():
    return render_template("pages/home.html")


@core_bp.route("/staff", strict_slashes=False)
@require_oauth()
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


@core_bp.route("/staff/<grade>", strict_slashes=False)
@require_oauth()
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
            grade_ext = "Relations Office Staff"
    return render_template("pages/staff.html", grade=grade, grade_ext=grade_ext)


@core_bp.route("/files", strict_slashes=False)
@require_oauth()
def files_route_generic():
    # landing_route_kg = url_for("pages.core.files_route", grade="kg")
    # landing_route_el = url_for("pages.core.files_route", grade="el")
    # landing_route_jh = url_for("pages.core.files_route", grade="jh")
    # landing_route_sh = url_for("pages.core.files_route", grade="sh")
    landing_route_kg = ImportantFiles.query.filter_by(grade="KG").one_or_404().url
    landing_route_el = ImportantFiles.query.filter_by(grade="EL").one_or_404().url
    landing_route_jh = ImportantFiles.query.filter_by(grade="JH").one_or_404().url
    landing_route_sh = ImportantFiles.query.filter_by(grade="SH").one_or_404().url
    return render_template(
        "pages/landing.html",
        type="Important Files",
        landing_route_kg=landing_route_kg,
        landing_route_el=landing_route_el,
        landing_route_jh=landing_route_jh,
        landing_route_sh=landing_route_sh
    )
    

@core_bp.route("/files/<grade>", strict_slashes=False)
@require_oauth()
def files_route(grade: str):
    grade = grade.lower()
    grade_ext = ""
    match grade:
        case "kg":
            grade_ext = "Kindergarten Files"
        case "el":
            grade_ext = "Elementary Files"
        case "jh":
            grade_ext = "Junior High Files"
        case _:
            grade_ext = "Senior High Files"
    return render_template("pages/files.html", grade=grade, grade_ext=grade_ext)


@core_bp.route("/term-overview", strict_slashes=False)
@require_oauth()
def term_overview_route_generic():
    landing_route_kg = TermOverview.query.filter_by(grade="KG").one_or_404().url
    landing_route_el = TermOverview.query.filter_by(grade="EL").one_or_404().url
    landing_route_jh = TermOverview.query.filter_by(grade="JH").one_or_404().url
    landing_route_sh = TermOverview.query.filter_by(grade="SH").one_or_404().url
    return render_template(
        "pages/landing.html",
        type="Term Overview",
        landing_route_kg=landing_route_kg,
        landing_route_el=landing_route_el,
        landing_route_jh=landing_route_jh,
        landing_route_sh=landing_route_sh
    )
    
    
@core_bp.route("/academic-calendar", strict_slashes=False)
@require_oauth()
def academic_calendar_route_generic():
    landing_route_kg = AcademicCalendar.query.filter_by(grade="KG").one_or_404().url
    landing_route_el = AcademicCalendar.query.filter_by(grade="EL").one_or_404().url
    landing_route_jh = AcademicCalendar.query.filter_by(grade="JH").one_or_404().url
    landing_route_sh = AcademicCalendar.query.filter_by(grade="SH").one_or_404().url
    return render_template(
        "pages/landing.html",
        type="Academic Calendar",
        landing_route_kg=landing_route_kg,
        landing_route_el=landing_route_el,
        landing_route_jh=landing_route_jh,
        landing_route_sh=landing_route_sh
    )
    
    
@core_bp.route("/timetable", strict_slashes=False)
@require_oauth()
def timetable_route_generic():
    landing_route_kg = Timetable.query.filter_by(grade="KG").one_or_404().url
    landing_route_el = Timetable.query.filter_by(grade="EL").one_or_404().url
    landing_route_jh = Timetable.query.filter_by(grade="JH").one_or_404().url
    landing_route_sh = Timetable.query.filter_by(grade="SH").one_or_404().url
    return render_template(
        "pages/landing.html",
        type="Timetable",
        landing_route_kg=landing_route_kg,
        landing_route_el=landing_route_el,
        landing_route_jh=landing_route_jh,
        landing_route_sh=landing_route_sh
    )


@core_bp.route("/core-values")
@require_oauth()
def core_values_route():
    return render_template("pages/core_values.html")


@core_bp.route("/test", strict_slashes=False)
def test_route():
    return render_template("pages/test.html")


@core_bp.route("/admin", strict_slashes=False)
@require_oauth(admin_only=True)
def admin_route():
    return render_template("pages/admin.html")


@core_bp.route("/magolor", strict_slashes=False)
@require_oauth()
def magolor():
    return render_template("pages/magolor.html")
