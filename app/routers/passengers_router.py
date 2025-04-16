from typing import Annotated
from fastapi import APIRouter, HTTPException, Path, Query, status

from app.crud.passengers_crud import deletePassenger, getAllPassengers, getPassengerById
from ..db.fake_db import passengers_db
from app.models.passenger_model import Passenger

router = APIRouter(
    prefix="/passengers",
    tags=["Passenger"],
)


@router.get("/", response_model=False)
async def get_all_passengers() -> list[Passenger] | dict:
    passengers = await getAllPassengers()
    if passengers:
        return passengers
    return {"message": "Passengers still empty"}


@router.get("/{passenger_id}")
async def get_passenger_by_id(passenger_id: Annotated[int, Path(gt=0)]) -> Passenger:
    passenger = await getPassengerById(passenger_id)
    return passenger


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_passanger(passenger: Passenger) -> Passenger:
    new_passenger = Passenger.model_validate(passenger)
    passengers_db.append(new_passenger)
    return new_passenger


@router.delete("/{passenger_id}", response_model_exclude={"id"})
async def delete_passenger(passenger_id: Annotated[int, Path(gt=0)]) -> Passenger:
    passenger = await getPassengerById(passenger_id)
    await deletePassenger(passenger)
    return passenger
