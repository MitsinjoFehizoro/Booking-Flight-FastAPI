from typing import Annotated, Literal
from pydantic import BaseModel, Field, PositiveFloat, computed_field
from ..db.fake_db import bookings_db

from app.models.flight_model import Flight
from app.models.passenger_model import Passenger


class Booking(BaseModel):
    id: Annotated[int, Field(strict=True)] = 0  # A cause du fake_db
    passenger: Passenger
    flight: Flight
    travel_class: Literal["economy", "business", "first"]
    price: PositiveFloat


class BookingRequest(BaseModel):
    travel_class: Literal["economy", "business", "first"]
    price: PositiveFloat
