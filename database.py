from sqlmodel import Session, create_engine
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = "sqlite:///./anime.db"

ONLINE_DATABASE_URL= os.getenv("ONLINE_DATABASE_URL")

# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

engine = create_engine(ONLINE_DATABASE_URL, echo=True)

# Get a session
def get_session():
    with Session(engine) as session:
        yield session