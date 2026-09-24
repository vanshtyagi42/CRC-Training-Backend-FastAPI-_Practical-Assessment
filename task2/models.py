from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import field_validator, EmailStr

ALLOWED_EVENT_STATUSES = ["Open", "Closed"]


class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=100)
    venue: str = Field(min_length=1, max_length=100)
    capacity: int = Field(gt=0)
    organizer: str = Field(min_length=1, max_length=100)
    status: str = Field(default="Open")

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        if value not in ALLOWED_EVENT_STATUSES:
            raise ValueError(f"status must be one of {ALLOWED_EVENT_STATUSES}")
        return value


class Reservation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    event_id: int = Field(foreign_key="event.id")
    student_name: str = Field(min_length=1, max_length=100)
    roll_number: str = Field(min_length=1, max_length=50)
    email: EmailStr 