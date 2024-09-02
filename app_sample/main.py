from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
from concurrent.futures import ThreadPoolExecutor

app = FastAPI()

mylist = [
    {"id": 1, "name": "Alice", "age": 25, "city": "New York"},
    {"id": 2, "name": "Bob", "age": 30, "city": "Los Angeles"},
    {"id": 3, "name": "Charlie", "age": 35, "city": "Chicago"},
    {"id": 4, "name": "David", "age": 40, "city": "Houston"},
    {"id": 5, "name": "Eve", "age": 45, "city": "Phoenix"},
    {"id": 6, "name": "Frank", "age": 50, "city": "Philadelphia"},
    {"id": 7, "name": "Grace", "age": 55, "city": "San Antonio"},
    {"id": 8, "name": "Helen", "age": 60, "city": "San Diego"},
    {"id": 9, "name": "Ivy", "age": 65, "city": "Dallas"},
    {"id": 10, "name": "Jack", "age": 70, "city": "San Jose"}
]

class Item(BaseModel):
    id: int = None
    name: str
    age: int
    city: str


@app.get("/")
async def root():
    return mylist

@app.get('/{id}')
async def get_item(id: int):
    return [i for i in mylist if i['id'] == id]

@app.post('/')
async def post_root(item: Item):
    try:
        item.id = len(mylist) + 1
        mylist.append(item.model_dump())
    except Exception as e:
        return {"error": f"{e}"}
    return mylist

@app.delete('/{id}')
async def delete_item(id: int):
    mylist.remove((await get_item(id))[0])
    return mylist

@app.put('/{id}')
async def put_item(id: int, item: Item):
    i = ((await get_item(id))[0])
    new_item = item.model_dump()
    new_item['id'] = i['id']
    i.update(new_item)
    return mylist