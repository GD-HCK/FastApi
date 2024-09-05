from fastapi import FastAPI
from app_sample.configuration import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from routes.person_controller import router

USERNAME = config['connection_string']['username']
PASSWORD = config['connection_string']['password']
SERVER = config['connection_string']['server']
DATABASE = config['connection_string']['database']
DRIVER = config['connection_string']['driver'].replace(" ", "+")
DATABASE_URL = f'mssql+pyodbc://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver={DRIVER}'

app = FastAPI()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app.include_router(router)