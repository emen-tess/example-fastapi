# Reference:https://fastapi.tiangolo.com/tutorial/sql-databases/

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2 
from psycopg2.extras import RealDictCursor
import time
from .config import settings 


# connection string to access DB driver (SQLalchemy)
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:admin@localhost:5432/fastapi'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# create engine # responsible sqlalchemy to connect/to establish connection 
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# create session for talk to DB 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind= engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

"""
while True: 
    try:
        # environment variable instead hardcode 
        conn = psycopg2.connect(host = 'localhost', database='fastapi', user='postgres', 
        password='admin', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print ('database connection was succesfull!')
        break 
    except Exception as error:
        print ('database connection failed!')   
        print ('Error:', error)
        time.sleep(2)
"""
