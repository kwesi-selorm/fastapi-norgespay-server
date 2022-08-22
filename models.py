import datetime
from typing import List

from beanie import Document, Link
from pydantic import BaseModel, Field


class UserEntry(BaseModel):
    username: str
    email: str
    password: str
    confirm_password: str


class NewSalaryEntry(BaseModel):
    city: str
    company: str
    experience: int
    jobTitle: str
    salary: int
    sector: str
    userId: str


class UserLogin(BaseModel):
    username: str
    password: str


class User(Document):
    username: str
    email: str
    password_hash: str

    class Settings:
        name = "users"


class Salary(Document):
    city: str
    company: str
    experience: int
    job_title: str = Field(alias="jobTitle")
    previous_salaries: List[int] = Field(alias="previousSalaries")
    salary: int
    sector: str
    user: Link[User]
    created_at: datetime.datetime | None = Field(alias="createdAt")
    updated_at: datetime.datetime = Field(alias="updatedAt")

    class Settings:
        name = "salaries"

    class Config:
        arbitrary_types_allowed = True
