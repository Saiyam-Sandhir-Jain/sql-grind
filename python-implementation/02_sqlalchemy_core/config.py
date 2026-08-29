import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

DEFAULT_DATABASE_URL = "postgresql+psycopg://{role_name}:{password}@{hostname}:{port}/university"
DATABASE_URL = os.environ.get("DATABASE_URL_SQLALCHEMY", DEFAULT_DATABASE_URL)