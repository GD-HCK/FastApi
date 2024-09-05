from app_sample.configuration import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

USERNAME = config['connection_string']['username']
PASSWORD = config['connection_string']['password']
SERVER = config['connection_string']['server']
DATABASE = config['connection_string']['database']
DRIVER = config['connection_string']['driver'].replace(" ", "+")
DATABASE_URL = f'mssql+pyodbc://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver={DRIVER}'

engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()