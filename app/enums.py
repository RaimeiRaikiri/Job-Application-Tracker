from enum import Enum

class ApplicationStatus(str, Enum):
    APPLIED = "Applied"
    ASSESSMENT = "Assessment"
    INTERVIEW = "Interview"
    REJECTED = "Rejected"
    WITHDRAWN = "Withdrawn"
    
class InterviewStage(str, Enum):
    PHONE_SCREEN = "Phone Screen"
    TECHNICAL = "Technical Interview"
    FINAL = "Offer"
    
# Could use Enums for job title