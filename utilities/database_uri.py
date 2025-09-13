from dotenv import load_dotenv
from flask import current_app

import os
from pathlib import Path


def get_database_uri(app):  # deprecated
    return app.config.get("SQLALCHEMY_DATABASE_URI", "sqlite:///instance/database.db")
