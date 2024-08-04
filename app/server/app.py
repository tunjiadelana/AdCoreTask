#create a default route
from fastapi import FastAPI , Request
from datetime import datetime, date, time , timezone
from server.routes.course import Loaddata, router as CourseRouter
from starlette.middleware.base import BaseHTTPMiddleware

from server.database import (
     Check_Load_courses,
)
description = """
This API helps you to perform CRUD operations on data related to courses. 🚀

## Items

You will be able to:

* **Fetch all courses **.
* **Fetch individual courses by ID**.
* **Update courses by ID **.
* **Delete courses by ID**.
"""
app = FastAPI(title="Course Management",
    description=description,
    summary="Adelana Oyetunji's assignment.",
    version="0.0.1",
    contact={
        "name": "Adelana Oyetunji",
        "email": "Tunjiadelana@yahoo.com",
    },
   )

app.add_middleware(BaseHTTPMiddleware, dispatch=Loaddata)


app.include_router(CourseRouter, tags=["Course"], prefix="/Course")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this Adcore interview task, by Adelana Oyetunji"}

