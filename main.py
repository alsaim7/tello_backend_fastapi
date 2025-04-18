from fastapi import FastAPI
import model
import database
from routers import animeList
from fastapi.middleware.cors import CORSMiddleware
from routers import user
from routers import authentication

app= FastAPI()

# Create tables
def create_db_and_tables():
    model.SQLModel.metadata.create_all(database.engine)

create_db_and_tables()

app.include_router(animeList.router)
app.include_router(user.router)
app.include_router(authentication.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://mytello.netlify.app","http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)