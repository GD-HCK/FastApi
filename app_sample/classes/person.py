from pydantic import BaseModel
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
import requests
from sqlalchemy import Column, Integer, String
from http import HTTPStatus
from sqlalchemy.orm import Session
from db import Base
from uuid import UUID

# Pydantic models
class PersonSchema(BaseModel):
    name: UUID | None = None
    age: int
    city: str
    state: str
    country: str
    address: str

    class Config:
        orm_mode = True

    
class Person(Base):

    __tablename__ = "users"
    
    id = Column(UNIQUEIDENTIFIER, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    address = Column(String)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
    
    @classmethod
    def get_all(cls, db: Session):
        return db.query(cls).all()
    
    @classmethod
    async def get_person (
        cls,
        db: Session,
        id: int | None = None, # Annotated[int | None, Query(ge=0,lt=130)] = None
        name: str | None = None, 
        age: int | None = None, 
        city: str | None = None, 
        state: str | None = None, 
        country: str | None = None, 
        address: str | None = None
        ):
        query = db.query(cls)
        
        if id is not None:
            query = query.filter(cls.id == id)
        
        if name is not None:
            query = query.filter(cls.name.ilike(f"%{name}%"))
        
        if age is not None:
            query = query.filter(cls.age == age)
        
        if city is not None:
            query = query.filter(cls.city.ilike(f"%{city}%"))
        
        if state is not None:
            query = query.filter(cls.state.ilike(f"%{state}%"))
        
        if country is not None:
            query = query.filter(cls.country.ilike(f"%{country}%"))
        
        if address is not None:
            query = query.filter(cls.address.ilike(f"%{address}%"))
        
        return query.all()

    @classmethod
    async def add_person(cls, db: Session, person_data: dict):
        try:
            person = cls.from_dict(person_data)
            db.add(person)
            db.commit()
            db.refresh(person)
        except Exception as e:
            db.rollback()
            return {"error": f"{e}", "status": HTTPStatus.INTERNAL_SERVER_ERROR}
        return {"status": HTTPStatus.CREATED, "person": person}

    @classmethod
    async def delete_person(cls, db: Session, id: str):
        try:
            person = db.query(cls).filter(cls.id == id).first()
            if not person:
                return {"error": f"Person with id {id} not found", "status": HTTPStatus.NOT_FOUND}
            db.delete(person)
            db.commit()
        except Exception as e:
            db.rollback()
            return {"error": f"{e}", "status": HTTPStatus.INTERNAL_SERVER_ERROR}
        return {"status": HTTPStatus.OK, "id": id}
    
    @classmethod
    async def update_person(cls, db: Session, id: str, person_data: dict):
        try:
            person = db.query(cls).filter(cls.id == id).first()
            if not person:
                return {"error": f"Person with id {id} not found", "status": HTTPStatus.NOT_FOUND}
            
            for key, value in person_data.items():
                setattr(person, key, value)
            
            db.commit()
            db.refresh(person)
        except Exception as e:
            db.rollback()
            return {"error": f"{e}", "status": HTTPStatus.INTERNAL_SERVER_ERROR}
        return {"status": HTTPStatus.OK, "person": person}