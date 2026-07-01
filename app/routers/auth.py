from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from app.database import get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import app.models as models
from app.schemas import UserInDB, Token, CurrentUser
from datetime import timedelta, datetime
from jose import jwt, JWTError
import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM="HS256"
TOKEN_EXPIRE_TIME=30

router = APIRouter(prefix="/auth", tags=["Auth"])

db_dependency = Annotated[Session , Depends(get_db)]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_context = OAuth2PasswordBearer(tokenUrl="/auth/token")

def hash_password(password):
    return pwd_context.hash(password)
    
def verify_password(plain_password ,hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(username, db: db_dependency):
    user = db.query(models.User).filter(models.User.username == username).first()
    
    if user:
        return UserInDB.model_validate(user)
    

def authenticate_user(username, password, db: db_dependency):
    user = get_user(username, db)
    
    if not user:
        return False
    if not verify_password(password, user.password):
        return False

    return user

def create_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

async def get_current_user(db: db_dependency, token: str = Depends(oauth2_context)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
    except JWTError:
        raise credential_exception
    
    if not username:
        raise credential_exception
    
    user = get_user(username, db)
    
    if not user:
        raise credential_exception
    
    
    return CurrentUser(username=user.username)

    
@router.post("/token", response_model=Token)
def login_for_access_token(db: db_dependency, form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password, db)
    
    if user:
        token = create_token(
            data={"sub":user.username},
            expires_delta=timedelta(minutes=TOKEN_EXPIRE_TIME),
            )
        
        if token:
            return Token(access_token=token, token_type="bearer")
        
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect user or password",
        headers={"WWW-Authenticate": "Bearer"},
    )