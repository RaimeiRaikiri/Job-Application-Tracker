from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from app.enums import ApplicationStatus, InterviewStage

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    
    applications = relationship("Application", back_populates="user" )
    

class Application(Base):
    __tablename__ = "application"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    job_id = Column(Integer, ForeignKey("job.id"))
    date_applied = Column(Date)
    status = Column(Enum(ApplicationStatus))
    
    user = relationship("User", back_populates="applications")
    job = relationship("Job", back_populates="applications")
    offer = relationship("Offer", back_populates="application")
    
    interviews = relationship("Interview", back_populates="application")
    notes = relationship("Note", back_populates="application")
    documents = relationship("Document", back_populates="application")
   
    history = relationship("Application_History", back_populates="application")


class Company(Base):
    __tablename__ = "company"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    website = Column(String)
    industry = Column(String) # Potential Enum
    location = Column(String) # Potentially many locations
    
    jobs = relationship("Job", back_populates="company")


class Offer(Base):
    __tablename__ = "offer"
    
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("application.id"))
    salary = Column(String)
    start_date = Column(Date)
    accepted = Column(Boolean)
    
    application = relationship("Application", back_populates="offer")

class Note(Base):
    __tablename__ = "note"
    
    id = Column(Integer, primary_key=True, index=True)
    applicaion_id = Column(Integer, ForeignKey("application.id"))
    content = Column(String)
    created_at = Column(DateTime)
    
    application = relationship("Application", back_populates="notes")
    pass

class Document(Base):
    __tablename__ = "document"
    
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("application.id"))
    filename = Column(String)
    storage_path = Column(String)
    uploaded_at = Column(DateTime)
    application = relationship("Application", back_populates="doucments")


class Job(Base):
    __tablename__ = "job"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("company.id"))
    title = Column(String)
    salary = Column(String)
    remote = Column(Boolean)
    description = Column(String)

    company = relationship("Company", back_populates="jobs")
    applications = relationship("Application", back_populates="job")
    
class Interview(Base):
    __tablename__ = "interview"
    
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("application.id"))
    stage = Column(Enum(InterviewStage))
    scheduled_at = Column(DateTime)
    result = Column(String)
    
    application = relationship("Application", back_populates="interviews")
    
class Application_History(Base):
    __tablename__ = "application_status_history"
    
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("application.id"))
    old_status = Column(Enum(ApplicationStatus))
    new_status = Column(Enum(ApplicationStatus))
    changed_at = Column(Date)
    
    application = relationship("Application", back_populates="history")