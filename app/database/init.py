from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

db_url = os.getenv("DB_URL")

if db_url is None:
    raise ValueError("Database URL hasn't been found")

engine = create_engine(
    url=db_url,
    echo=True
)

session_fabric = sessionmaker(engine)