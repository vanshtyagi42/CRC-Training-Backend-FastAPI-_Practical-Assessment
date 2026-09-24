from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import field_validator

ALLOWED_STATUSES = ["Lost", "Found", "Returned"]

class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    title: str = Field(min_length=3, max_length=100)

    description: str = Field(min_length=5, max_length=500)

    category: str = Field(min_length=1, max_length=50)

    location: str = Field(min_length=1, max_length=100)

    reported_by: str = Field(min_length=1, max_length=100)

    status: str = Field(default="Lost")

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        if value not in ALLOWED_STATUSES:
            raise ValueError(f"status must be one of {ALLOWED_STATUSES}")
        return value 