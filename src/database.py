from databases import Database
from sqlalchemy import create_engine
from src.config import SQL_URL

db = Database(SQL_URL)
engine= create_engine(SQL_URL)