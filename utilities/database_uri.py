from dotenv import load_dotenv

import os
from pathlib import Path


def get_database_uri():
    base_dir = Path(__file__).resolve().parent.parent.parent.parent
    env_file_path = base_dir / ".env"
    load_dotenv(env_file_path)
    return os.environ.get("DATABASE_URI", "sqlite:///instance/database.db")
