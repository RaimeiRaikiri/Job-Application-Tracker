from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app.schemas import CurrentUser, ApplicationCreate, Application, ApplicationResponse, ApplicationUpdate
from app.routers.auth import get_current_user
from app import models
from datetime import date, datetime
from app.enums import ApplicationStatus


router = APIRouter(prefix="/applications", tags=["Applications"])

db_dependency = Annotated[Session, Depends(get_db)]
current_user = Annotated[CurrentUser, Depends(get_current_user)]

@router.post("/", response_model=Application, status_code=status.HTTP_201_CREATED)
def create_application(
    application: ApplicationCreate,
    db: db_dependency,
    current_user: current_user
    ):
    # Create company if it doesn't exist
    company = db.query(models.Company).filter(models.Company.name == application.company_name.lower()).first()
    
    if not company:
        company = models.Company(
            name=application.company_name.lower(),
            website=application.company_website,
            industry=application.company_industry,
            location=application.company_location
        )
        
        db.add(company)
        db.commit()
        db.refresh(company)
        
    # Create job if it doesn't exist
    job = db.query(models.Job).filter(models.Job.title == application.job_title.lower()).first()
    
    if not job:
        job = models.Job(
            company_id=company.id,
            title=application.job_title,
            salary=application.job_salary,
            remote=application.job_remote,
            description=application.job_description
        )
        
        db.add(job)
        db.commit()
        db.refresh(job)

    
    new_application = models.Application(
        date_applied=date.today(),
        status=ApplicationStatus.APPLIED,
        user_id=current_user.id,
        job_id=job.id
    )
    
    try:
        db.add(new_application)
        db.commit()
        db.refresh(new_application)
        
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid application data"
        )
    
    return Application.model_validate(new_application)

@router.get("/", response_model=list[ApplicationResponse])
def get_applications(db: db_dependency, current_user: current_user):
    applications = db.query(models.Application).filter(models.Application.user_id == current_user.id).all()
    
    return applications

@router.get("/{application_id}", response_model=ApplicationResponse)
def get_application_by_id(application_id, db: db_dependency, current_user: current_user):
    application = db.query(models.Application).filter(models.Application.id == application_id).first()
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application {application_id} not found"
            )
    
    if application.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to access this application"
            )
    
    
    return ApplicationResponse.model_validate(application)

@router.put("/{application_id}", response_model=ApplicationResponse)
def update_application(application_id, updated_application: ApplicationUpdate, db: db_dependency, current_user: current_user):
    application = db.query(models.Application).filter(models.Application.id == application_id).first()
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application {application_id} not found"
            )
    
    if application.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to update this application"
        )

    if updated_application.status:
        history = models.Application_History(
            application_id=application.id,
            old_status=application.status,
            new_status=updated_application.status.lower(),
            changed_at=datetime.now()
        )
        
        application.status = updated_application.status.lower()
        
        
    db.commit()
    db.refresh(application)
    
    db.add(history)
    db.commit()

    return ApplicationResponse.model_validate(application)
    
@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(application_id, db: db_dependency, current_user: current_user):
    application = db.query(models.Application).filter(models.Application.id == application_id).first()
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application {application_id} not found"
            )
    if application.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to delete this application"
            )
    
    db.delete(application)
    db.commit()
    
    return 
        