from fastapi import APIRouter, HTTPException, status
from typing import List
from beanie import PydanticObjectId
from datetime import datetime
from fastapi.encoders import jsonable_encoder

from models import NewSalaryEntry, Salary, User

router = APIRouter(tags=["Salaries"])

# GET ALL SALARIES
@router.get(
    "/api/salaries/all",
    response_description="All salaries fetched",
    response_model=List[Salary],
)
async def find_salaries() -> List[Salary]:
    """
    GET ALL SALARIES
    """
    documents = await Salary.find({}).to_list()
    if documents:
        return documents
    raise HTTPException(404, "No salaries found")


# GET SALARY USING ID PARAMETER
@router.get(
    "/api/salaries/{id}",
    response_description="Returned salary",
)
async def find_one_salary(id: str):
    """
    GET ONE SALARY
    """
    try:
        document = await Salary.get(PydanticObjectId(id))
        return document
    except Exception:
        raise HTTPException(404, "The requested salary was not found")


# INSERT NEW SALARY
@router.post("/api/salaries", status_code=status.HTTP_201_CREATED)
async def create_salary(payload: NewSalaryEntry):
    """
    POST SALARY
    """
    json_payload: dict = jsonable_encoder(payload)  # CONVERT TO JSON OBJECT
    document = json_payload
    document["createdAt"] = datetime.now()
    document["updatedAt"] = datetime.now()
    document["previousSalaries"] = [json_payload["salary"]]
    adding_user = await User.get(PydanticObjectId(json_payload["userId"]))
    adding_user_json: dict = jsonable_encoder(adding_user)
    document["user"] = adding_user_json["_id"]
    document_to_create = Salary(**document)

    try:
        await Salary.create(document_to_create)
        return document_to_create
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to add new salary entry")
