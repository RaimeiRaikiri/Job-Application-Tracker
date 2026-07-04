from enum import Enum

class ApplicationStatus(str, Enum):
    APPLIED = "applied"
    ASSESSMENT = "assessment"
    INTERVIEW = "interview"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"
    
class InterviewStage(str, Enum):
    PHONE_SCREEN = "phone_screen"
    TECHNICAL = "technical_interview"
    FINAL = "offer"
    
# Could use Enums for job title