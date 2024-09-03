from typing import Annotated
from fastapi import FastAPI, Query
from pydantic import BaseModel
import asyncio
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
import requests

app = FastAPI()

class Person(BaseModel):
    id: int = None
    name: str
    age: int
    city: str
    state: str
    country: str
    address: str

# people = [
#     {"id": 1, "name": "Alice", "age": 25, "city": "New York"},
#     {"id": 2, "name": "Bob", "age": 30, "city": "Los Angeles"},
#     {"id": 3, "name": "Charlie", "age": 35, "city": "Chicago"},
#     {"id": 4, "name": "David", "age": 40, "city": "Houston"},
#     {"id": 5, "name": "Eve", "age": 45, "city": "Phoenix"},
#     {"id": 6, "name": "Frank", "age": 50, "city": "Philadelphia"},
#     {"id": 7, "name": "Grace", "age": 55, "city": "San Antonio"},
#     {"id": 8, "name": "Helen", "age": 60, "city": "San Diego"},
#     {"id": 9, "name": "Ivy", "age": 65, "city": "Dallas"},
#     {"id": 10, "name": "Jack", "age": 70, "city": "San Jose"}
# ]

def fetch_random_users(count):
    url = f"https://randomuser.me/api/?results={count}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['results']
    else:
        raise Exception(response.json()['error'])

def generate_large_list(size):
    users = fetch_random_users(size)
    large_list = []
    for i, user in enumerate(users, start=1):
        address = f"{', '.join(str(v) for k,v in user['location']['street'].items())}, {user['location']['city']}, {user['location']['state']}, {user['location']['country']}"
        entry = {
            'id': i,
            'name': ' '.join(v for k,v in user['name'].items()),
            'age': user['dob']['age'],
            'city': user['location']['city'],
            'state': user['location']['state'],
            'country': user['location']['country'],
            'address': address
        }
        large_list.append(entry)
    return large_list

try:
    people = generate_large_list(5000)  # Adjust the size as needed
    error_msg = ""
except Exception as e:
    error_msg = f'There was an issue request random users via API: {e}'
    people = []
    print(f"Error: {e}")

@app.get("/")
async def root():
    if error_msg:
        return {"error": error_msg}
    return people

@app.get('/person/')
async def get_person(
    id: int | None = None, # Annotated[int | None, Query(ge=0,lt=130)] = None
    name: str | None = None, 
    age: int | None = None, 
    city: str | None = None, 
    state: str | None = None, 
    country: str | None = None, 
    address: str | None = None
    ):
    if error_msg:
        return {"error": error_msg}
    
    filtered_people = people
    
    if id is not None:
        filtered_people = [person for person in filtered_people if person["id"] == id]
    
    if name is not None:
        filtered_people = [person for person in filtered_people if name.lower() in person["name"].lower()]
    
    if age is not None:
        filtered_people = [person for person in filtered_people if person["age"] == age]
    
    if city is not None:
        filtered_people = [person for person in filtered_people if city.lower() in person["city"].lower()]
    
    if state is not None:
        filtered_people = [person for person in filtered_people if state.lower() in person["state"].lower()]
    
    if country is not None:
        filtered_people = [person for person in filtered_people if country.lower() in person["country"].lower()]
    
    if address is not None:
        filtered_people = [person for person in filtered_people if address.lower() in person["address"].lower()]
    
    return filtered_people

@app.post('/')
async def post_root(person: Person):
    if error_msg:
        return {"error": error_msg}
    
    try:
        person.id = len(people) + 1
        people.append(person.model_dump())
    except Exception as e:
        return {"error": f"{e}"}
    return people

@app.delete('/{id}')
async def delete_person(id: int):
    if error_msg:
        return {"error": error_msg}
    
    people.remove((await get_person(id))[0])
    return people

@app.put('/{id}')
async def put_person(id: int, person: Person):
    if error_msg:
        return {"error": error_msg}
    
    i = ((await get_person(id))[0])
    new_person = person.model_dump()
    new_person['id'] = i['id']
    i.update(new_person)
    return people