from fastapi import FastAPI
from routes.person_controller import router

app = FastAPI()
app.include_router(router)