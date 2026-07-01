from pydantic import BaseModel, EmailStr, Field, ConfigDict
from app.enums import ApplicationStatus

class ApplicationBase(BaseModel):
    pass

class ApplicationCreate(BaseModel):
    pass
class Token(BaseModel):
    access_token: str
    token_type: str
    
class CurrentUser(BaseModel):
    username: str 
    
class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    email: EmailStr
    
class UserCreate(UserBase):
    password: str = Field(min_length=8)
    
class UserResponse(UserBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

class UserInDB(UserBase):
    id: int
    password: str
    
    model_config = ConfigDict(from_attributes=True)

