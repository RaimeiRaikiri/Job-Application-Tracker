from fastapi import FastAPI
from app.models import Base
from app.database import engine
from app.routers import auth, users, applications

app = FastAPI(
    title="Job application tracker",
    description="Tracks job applications",
    version="1.0.0"
)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(applications.router)