from fastapi import FastAPI
from app.models import Base
from app.database import engine

app = FastAPI(
    title="Job application tracker",
    description="Tracks job applications",
    version="1.0.0"
)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)