from flask import current_app, redirect, url_for, render_template, session
from flask_dance.contrib.google import google, make_google_blueprint
from flask_login import login_user

from app.extensions import db
from app.models.auth import User
from app.models.employee import Employee

from functools import wraps
import os


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
google_bp = make_google_blueprint(
    client_id=current_app.config["CLIENT_ID"],
    client_secret=current_app.config["CLIENT_SECRET"],
    scope=["https://www.googleapis.com/auth/userinfo.email",
           "openid",
           "https://www.googleapis.com/auth/userinfo.profile"],
    redirect_to="pages.core.home_route"  # Must include blueprint name
)


def require_oauth(admin_only=False):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not google.authorized:
                return redirect(url_for("pages.core.login_user"))
            
            try:
                resp = google.get("/oauth2/v2/userinfo")
                if not resp.ok:
                    pass  # implement later
                else:
                    user_info = resp.json()  # keys: name, email, picture
                    name = user_info["name"]
                    email = user_info["email"]
                    picture = user_info["picture"]
                    
                    # Create a new user entry in the DB, if needed
                    user = User.query.filter_by(email=email).one_or_none()
                    if not user:
                        user = User(email=email, name=name, password="placeholder")
                        db.session.add(user)
                        db.session.commit()
                    
                    # Store in session
                    login_user(user)
                    session['name'] = {'name': name}
                    session['user'] = {'email': email}
                    session['picture'] = {'picture': picture}
                    session.modified = True
                    
                    email_whitelist = "internship1@cpi.ipeka.sch.id"
                    if admin_only and Employee.query.filter_by(email=email).one_or_none() is None and email not in email_whitelist:
                        return render_template("oauth/admin_required.html", email=email, b1=str(admin_only), b2=str(Employee.query.filter_by(email=email).one_or_none() is None), b3=str(email != email_whitelist))
                    return f(*args, **kwargs)

            except Exception as e:
                # flash(f'An error occurred: {str(e)}', 'error')
                return redirect(url_for('pages.core.login_user'))
            
        return wrapper
    return decorator

