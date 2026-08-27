import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

DEFAULT_DB_URL = "postgresql://your_role:your_password@localhost:5432/university"
DATABASE_URL = os.environ.get("DATABASE_URL", DEFAULT_DB_URL)