from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from os import getenv
from dotenv import load_dotenv
load_dotenv()

engine = create_engine(getenv("DB_URL"))
print(getenv("DB_URL"))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

db = SessionLocal()

# def get_db():
#     try:
#         db = SessionLocal()
#         yield db
#     finally:
#         db.close()

