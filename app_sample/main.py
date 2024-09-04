from fastapi import FastAPI
from configuration import config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from routes.person_controller import router

DATABASE_URL = f'mssql+pyodbc://{config['connection_string']['username']}:{config['connection_string']['password']}@{config['connection_string']['server']}/{config['connection_string']['database']}?driver={config['connection_string']['driver'].replace(" ", "+")}'

app = FastAPI()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app.include_router(router)