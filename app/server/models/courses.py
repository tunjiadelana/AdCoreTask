# models for courses
from typing import Optional
from datetime import datetime, date, time , timezone
from pydantic import BaseModel, datetime_parse, Field
import uuid

class CourseSchemaExposed(BaseModel):
    University: str = Field(...)
    City: str = Field(...)
    Country: str  = Field(...)
    CourseName: str = Field(...)
    CourseDescription: str = Field(...)
    StartDate: date = Field(...)
    EndDate: date = Field(...)
    Price: float = Field(...)
    Currency: str = Field(...)
    
    class Config:
        schema_extra = {
            "example": {
                "University": "ABC Tech University",
                "City": "Toronto",
                "Country": "Canada",
                "CourseName": "Machine Learning",
                "CourseDescription": "A branch of AI",
                "StartDate": "02-Aug-2024",
                "EndDate": "02-Aug-2025",
                "Price": 8000,
                "Currency": "CAD",
            }
        }


class CourseSchema(BaseModel):
    University: str = ""
    City: str = ""
    Country: str  = ""
    CourseName: str = ""
    CourseDescription: str = ""
    StartDate: date = ""
    EndDate: date = ""
    Price: float = ""
    Currency: str = ""
    Tmstamp: datetime = datetime.now(timezone.utc)

    class Config:
        schema_extra = {
            "example": {
                "University": "ABC Tech University",
                "City": "Toronto",
                "Country": "Canada",
                "CourseName": "Machine Learning",
                "CourseDescription": "A branch of AI",
                "StartDate": "02-Aug-2024",
                "EndDate": "02-Aug-2025",
                "Price": 8000,
                "Currency": "CAD",
            }
        }

class UpdateCourseModel(BaseModel):
    University: Optional[str]
    City: Optional[str]
    Country: Optional[str]
    CourseName: Optional[str]
    CourseDescription: Optional[str]
    StartDate: Optional[date]
    EndDate: Optional[date]
    Price: Optional[float]
    Currency: Optional[str] 

    class Config:
        schema_extra = {
            "example": {
                "University": "ABC Tech University",
                "City": "Toronto",
                "Country": "Canada",
                "CourseName": "Machine Learning",
                "CourseDescription": "A branch of AI",
                "StartDate": "02-Aug-2024",
                "EndDate": "02-Aug-2025",
                "Price": 8000,
                "Currency": "CAD",
            }
        }

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message, 
        
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
