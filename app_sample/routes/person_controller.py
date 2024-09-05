from typing import Annotated, List
from classes.person import Person, PersonSchema
from sqlalchemy.orm import Session
from db import get_db
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()

@router.get("/", response_model=List[PersonSchema])
async def get_all(db: Session = Depends(get_db)):
    return Person.get_all(db)

@router.get('/person/', response_model=List[PersonSchema])
async def get_person(
    id: int | None = None, # Annotated[int | None, Query(ge=0,lt=130)] = None
    name: str | None = None, 
    age: int | None = None, 
    city: str | None = None, 
    state: str | None = None, 
    country: str | None = None, 
    address: str | None = None,
    db: Session = Depends(get_db)
):
    return await Person.get_person(db, id, name, age, city, state, country, address)

@router.post('/', response_model=PersonSchema)
async def add_person(person: PersonSchema, db: Session = Depends(get_db)):
    result = await Person.add_person(db, person.model_dumps())
    if "error" in result:
        raise HTTPException(status_code=result["status"], detail=result["error"])
    return result["person"]

@router.delete('/{id}')
async def delete_person(id: str, db: Session = Depends(get_db)):
    result = await Person.delete_person(db, id)
    if "error" in result:
        raise HTTPException(status_code=result["status"], detail=result["error"])
    return {"status": result["status"], "id": result["id"]}

@router.put('/{id}', response_model=PersonSchema)
async def update_person(id: str, person: PersonSchema, db: Session = Depends(get_db)):
    result = await Person.update_person(db, id, person.model_dumps())
    if "error" in result:
        raise HTTPException(status_code=result["status"], detail=result["error"])
    return result["person"]
