from array import array
from datetime import datetime
from typing import List
from pprint import pprint

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from models import SalaryAmount
from models import NewSalaryEntry, Salary, User

router = APIRouter(prefix="/api/salaries", tags=["Salaries"])

# tokenUrl is the parameter containing the relative URL that the client (frontend running in the user's browser) will use to send the username and password to get a token.
# e.g. With a tokenUrl parameter of 'token',
# http://example.com/ would refer to http://example.com/token
# https://example.com/api/v1 would refer to https://example.com/api/v1/token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")


# GET ALL SALARIES
@router.get(
    "/all",
    response_description="All salaries fetched",
    response_model=List[Salary],
)
async def find_salaries(token: str = Depends(oauth2_scheme)) -> List[Salary]:
    """
    GET ALL SALARIES
    """
    documents = await Salary.find({}).to_list()
    if documents:
        return documents
    raise HTTPException(404, "No salaries found")


# GET SALARY USING ID PARAMETER
@router.get(
    "/{id}",
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
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_salary(payload: NewSalaryEntry):
    """
    POST SALARY
    """
    # Add authorization method to determine if a user can create a new salary. User sends token and it is verified before proceeding
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


# UPDATE SINGLE SALARY
@router.put("/{id}")
async def update_single_salary(id: str, payload: SalaryAmount):
    to_update = await Salary.get(PydanticObjectId(id))
    if to_update is None:
        raise HTTPException(status_code=404, detail="Salary does not exist")
    to_update_dict: dict = jsonable_encoder(to_update)
    if payload.amount in to_update_dict["previousSalaries"]:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Sorry, the submitted salary is already available in the database",
        )
    to_update_dict["previousSalaries"].append(payload.amount)
    updated_salaries = to_update_dict["previousSalaries"]

    try:
        await to_update.set(
            {"salary": payload.amount, "previousSalaries": updated_salaries}
        )
        await to_update.save()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Salary update failed: {str(e)}")
