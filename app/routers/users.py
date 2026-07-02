from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserCreate, UserResponse, CurrentUser
from app.models import User
from app.routers.auth import hash_password, get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

db_dependency = Annotated[Session, Depends(get_db)]
current_user = Annotated[CurrentUser, Depends(get_current_user)]

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(new_user: UserCreate, db: db_dependency):

    # Check if user exists first
    existing_username = db.query(User).filter(User.username == new_user.username).first()
    
    if existing_username:
        # Raise exception for existing user already
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to create account"
        )
    
    existing_email = db.query(User).filter(User.email == new_user.email).first()
    
    if existing_email:
        # Raise exception for existing email already
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to create account"
        )
    
    hashed_password = hash_password(new_user.password)
    
    new_user.password = hashed_password
    
    db.add(User(**new_user.model_dump()))
    db.commit()
    
    user = db.query(User).filter(User.username == new_user.username).first()
    response = UserResponse.model_validate(user)
    
    return response

@router.get("/me", response_model=CurrentUser)
def get_user_details(current_user: current_user):
    return current_user
    