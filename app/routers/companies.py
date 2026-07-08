from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, status, HTTPException
from app.database import get_db
from app.routers.auth import get_current_user
from app.schemas import CurrentUser, CompanyCreate, CompanyResponse, CompanyUpdate
from app.models import Company

db_dependency = Annotated[Session, Depends(get_db)]
current_user = Annotated[CurrentUser, Depends(get_current_user)]

router = APIRouter(prefix="/companies", tags=["Companies"])

# _ is being used to make each endpoint protected, despite lack of requirement for specific current_user details
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CompanyResponse)
def create_company(company_details: CompanyCreate, db: db_dependency, _: current_user):
    
    company = db.query(Company).filter(Company.name == company_details.name).first()
    
    if not company:
        company = Company(
            name=company_details.name,
            website=company_details.website,
            industry=company_details.industry,
            location=company_details.location
        )
        
        db.add(company)
        db.commit()
        db.refresh(company)
    
    return CompanyResponse.model_validate(company)

@router.get("/", response_model=list[CompanyResponse])
def get_all_companies(db: db_dependency, _: current_user):
    return db.query(Company).all()
    
@router.get("/{company_id}", response_model=CompanyResponse)
def get_company_by_id(company_id: int, db: db_dependency, _: current_user):
    company = db.query(Company).filter(Company.id == company_id).first()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company {company_id} not found"
            )
    
    return CompanyResponse.model_validate(company)

@router.put("/{company_id}", response_model=CompanyResponse)
def update_company(company_id: int, company_update: CompanyUpdate, db: db_dependency, _: current_user):
    company = db.query(Company).filter(Company.id == company_id).first()
    
    if not company:
        raise  HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company {company_id} not found"
            )
        
    if company_update.website:
        company.website = company_update.website
    if company_update.industry:
        company.industry = company_update.industry
    if company_update.location:
        company.location = company_update.location
        
    db.commit()
    db.refresh(company)
    
    return CompanyResponse.model_validate(company)

@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company(company_id: int, db: db_dependency, _: current_user):
    company = db.query(Company).filter(Company.id == company_id).first()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company {company_id} not found"
            )
    
    db.delete(company)
    db.commit()
    
    return 