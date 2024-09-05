from pydantic import BaseModel
import requests
from http import HTTPStatus

class Person(BaseModel):
    id: int = None
    name: str
    age: int
    city: str
    state: str
    country: str
    address: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
    
    @classmethod
    def get_all(cls):
        return people
    
    @classmethod
    async def get_person (
        cls,
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
        
        filtered_people = Person.get_all()
        
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

    @classmethod
    async def add_person(cls, person):
        if error_msg:
            return {"error": error_msg}
        
        try:
            person.id = len(people) + 1
            people.append(person.model_dump())
        except Exception as e:
            return {"error": f"{e}", "status": HTTPStatus.INTERNAL_SERVER_ERROR}
        return {"status": HTTPStatus.CREATED, "person": person}

    @classmethod
    async def delete_person(cls, id: int):
        if error_msg:
            return {"error": error_msg, "status": HTTPStatus.BAD_REQUEST}
    
        try:
            people.remove((await Person.get_person(id))[0])
        except Exception as e:
            return {"error": f"{e}", "status": HTTPStatus.INTERNAL_SERVER_ERROR}
        return {"status": HTTPStatus.OK, "id": id}
    
    @classmethod
    async def update_person(cls, id: int, body):
        if error_msg:
            return {"error": error_msg}
        
        person = ((await Person.get_person(id))[0])
        new_person = person
        if not person:
            return {"error": f"Person with id {id} not found", "status": HTTPStatus.NOT_FOUND}
        for k,v in body:
            new_person[k] = v
        person.update(new_person)
        return {"status": HTTPStatus.OK, "person": person}
    

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
    people = generate_large_list(200)  # Adjust the size as needed
    error_msg = ""
except Exception as e:
    error_msg = f'There was an issue request random users via API: {e}'
    people = []
    print(f"Error: {e}")