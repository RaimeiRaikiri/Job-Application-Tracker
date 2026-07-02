from pydantic import BaseModel, EmailStr, Field, ConfigDict
from app.enums import ApplicationStatus
from datetime import date
from app.enums import ApplicationStatus


class ApplicationBase(BaseModel):
    date_applied: date
    status: ApplicationStatus

class ApplicationCreate(BaseModel):
    company_name: str
    company_website: str
    company_industry: str
    company_location: str
    
    job_title: str
    job_salary: int
    job_remote: str # Enum potential
    job_description: str
    
class Application(ApplicationBase):
    user_id: int
    job_id: int
    
    model_config = ConfigDict(from_attributes=True)
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class CurrentUser(BaseModel):
    id: int
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

