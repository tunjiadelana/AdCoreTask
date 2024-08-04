from fastapi import APIRouter, Request, Body
from fastapi.encoders import jsonable_encoder
from datetime import datetime
import uuid

from server.database import (
    add_course,
    delete_course,
    retrieve_course,
    retrieve_courses,
    update_course,
    Check_Load_courses,
)
from server.models.courses import (
    ErrorResponseModel,
    ResponseModel,
    CourseSchema,
    CourseSchemaExposed,
    UpdateCourseModel,
)

router = APIRouter()

async def Loaddata(request: Request, call_next):
      Check_Load_courses()    
      response = await call_next(request)
      return response 

@router.post("/", response_description="Course data added into the database")
async def add_course_data(courseExposed: CourseSchemaExposed = Body(...)):
    course = CourseSchema() 
    setattr(course,"City",courseExposed.City)
    setattr(course,"Country",courseExposed.Country)
    setattr(course,"CourseDescription",courseExposed.CourseDescription)

    setattr(course,"CourseName",courseExposed.CourseName)
    setattr(course,"Currency",courseExposed.Currency)
    setattr(course,"EndDate",courseExposed.EndDate)

    setattr(course,"Price",courseExposed.Price)
    setattr(course,"StartDate",courseExposed.StartDate)
    setattr(course,"University",courseExposed.University)
    #setattr(course,"Tmstamp",datetime.now())

   # course.City = courseExposed.City
   # course.Country = courseExposed.Country
   # course.CourseDescription = courseExposed.CourseDescription
   # course.CourseName = courseExposed.CourseName
   # course.Currency = courseExposed.Currency
   # course.EndDate = courseExposed.EndDate
   # course.Price = courseExposed.Price
   # course.StartDate = courseExposed.StartDate
   # course.University = courseExposed.University
   # course.Tmstamp = datetime.now()
    course = jsonable_encoder(course)
    new_course = await add_course(course)
    return ResponseModel(new_course, "course added successfully.")

@router.get("/", response_description="All Courses retrieved")
async def get_courses():
    courses = await retrieve_courses()
    if courses:
        return ResponseModel(courses, "Courses data retrieved successfully")
    return ResponseModel(courses, "Empty list returned")


@router.get("/{id}", response_description="course data retrieved")
async def get_singlecourse_data(id):
    course = await retrieve_course(id)
    if course:
        return ResponseModel(course, "course data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "course doesn't exist.")

@router.put("/{id}")
async def update_course_data(id: str, req: UpdateCourseModel = Body(...)):
    req = {k: v for k, v in dict(req) if v is not None}
    updated_course = await update_course(id, req)
    if updated_course:
        return ResponseModel(
            "Course with ID: {} name update is successful".format(id),
            "Course name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the course data.",
    )
@router.delete("/{id}", response_description="Course data deleted from the database")
async def delete_course_data(id: str):
    deleted_course = await delete_course(id)
    if deleted_course:
        return ResponseModel(
            "Course with ID: {} removed".format(id), "course deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Course with id {0} doesn't exist".format(id)
    )
