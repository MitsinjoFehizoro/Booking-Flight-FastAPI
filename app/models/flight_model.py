from datetime import datetime
import re
import string
from typing import Annotated, Any, Self
from fastapi import HTTPException, status
from pydantic import (
    BaseModel,
    Field,
    computed_field,
    field_validator,
    model_validator,
)
from ..db.fake_db import flights_db


class Flight(BaseModel):
    id: Annotated[int, Field(strict=True)] = 0  # A cause du fake_db
    flight_number: Annotated[str, Field(pattern=r"^[A-Z]{2}[0-9]{3,4}$")]
    airline: Annotated[str, Field(min_length=3, max_length=20)]
    departure: Annotated[str, Field(min_length=3, max_length=3)]
    arrival: Annotated[str, Field(min_length=3, max_length=3)]
    departure_time: datetime
    arrival_time: datetime

    @field_validator("flight_number", mode="before")
    @classmethod
    def validate_flight_number(cls, value: str) -> string:
        value: str = value.upper()
        if not re.fullmatch(pattern=r"^[A-Z]{2}[0-9]{3,4}$", string=value):
            raise ValueError(
                "Flight_number must have a form 2 letters with  3-4 number : AF505"
            )
        return value

    @field_validator("arrival", "departure", mode="after")
    @classmethod
    def upper_departure_arrival(cls, value: str) -> str:
        return value.upper()

    @model_validator(mode="after")
    def validate_arrival_time(self) -> Self:
        if self.arrival_time <= self.departure_time:
            raise ValueError("Arrival_time must be after departure_time")
        return self
