import motor.motor_asyncio
import pandas as pd
from bson.objectid import ObjectId
import pymongo

MONGO_DETAILS = "mongodb+srv://ABC1234:ABC1234@cluster0.9pfnkbv.mongodb.net/" 
#"mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.AdCoreTest

course_collection = database.get_collection("Courses") 

# helpers


def course_helper(course) -> dict:
    return {
        "id": str(course["_id"]),
        "University": course["University"],
        "City": course["City"],
        "Country": course["Country"],
        "CourseName": course["CourseName"],
        "StartDate": course["StartDate"],
        "EndDate": course["EndDate"],
        "Price": course["Price"],
        "Currency": course["Currency"],
    }

# Check and normalise data 
def remove_badchars(input_str):
    import unicodedata
    nkfd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nkfd_form.encode('ASCII', 'ignore')
    return only_ascii.decode('utf-8')

# Check if data has expired and reload to database
async def Check_Load_courses():
    courses = []
    async for course in course_collection.find():
        courses.append(course_helper(course))
    if courses.count() == 0:
       Allrecords = pd.read_csv('https://api.mockaroo.com/api/501b2790?count=100&key=8683a1c0',header=0,)
       if Allrecords.count() > 0:
          Allrecords['City']  =  Allrecords['City'].apply(remove_badchars)
          Allrecords['Country']  =  Allrecords['Country'].apply(remove_badchars)
          Allrecords['CourseName']  =  Allrecords['CourseName'].apply(remove_badchars)
          Allrecords['CourseDescription']  =  Allrecords['CourseDescription'].apply(remove_badchars)
          Allrecords.reset_index(inplace=True)
          data_dict = Allrecords.to_dict("records")
          course_collection.insert_many(data_dict)
         
    return

# Retrieve all courses present in the database
async def retrieve_courses():
    Check_Load_courses()
    courses = []
    async for course in course_collection.find():
        courses.append(course_helper(course))
    return courses


# Add a new course into the database
async def add_course(course_data: dict) -> dict:
    course_collection.create_index('Tmstamp',expireAfterSeconds=60)
    course = await course_collection.insert_one(course_data)
    new_course = await course_collection.find_one({"_id": course.inserted_id})
    return course_helper(new_course)


# Retrieve a course with a matching ID
async def retrieve_course(id: str) -> dict:
    course = await course_collection.find_one({"_id": ObjectId(id)})
    if course:
        return course_helper(course)


# Update a course with a matching ID
async def update_course(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    course = await course_collection.find_one({"_id": ObjectId(id)})
    if course:
        updated_course = await course_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_course:
            return True
        return False


# Delete a course from the database
async def delete_course(id: str):
    course = await course_collection.find_one({"_id": ObjectId(id)})
    if course:
        await course_collection.delete_one({"_id": ObjectId(id)})
        return True