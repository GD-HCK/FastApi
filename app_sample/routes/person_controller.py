from typing import Annotated
from classes.person import Person, people, error_msg
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()

@router.get("/")
async def get_all():
    if error_msg:
        return {"error": error_msg}
    return Person.get_all()

@router.get('/person/')
async def get_person(
    id: int | None = None, # Annotated[int | None, Query(ge=0,lt=130)] = None
    name: str | None = None, 
    age: int | None = None, 
    city: str | None = None, 
    state: str | None = None, 
    country: str | None = None, 
    address: str | None = None
    ):
    return await Person.get_person(id, name, age, city, state, country, address)

@router.post('/')
async def add_person(person: Person):
    return await Person.add_person(person)

@router.delete('/{id}')
async def delete_person(id: int):
    return await Person.delete_person(id)

@router.put('/{id}')
async def update_person(id: int, person: Person):
    return await Person.update_person(id, person)
