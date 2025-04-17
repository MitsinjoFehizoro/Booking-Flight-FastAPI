from fastapi import HTTPException
from app.models.passenger_model import Passenger
from ..db.fake_db import passengers_db


async def getAllPassengers() -> list[Passenger] | None:
    if len(passengers_db) == 0:
        return None
    return passengers_db


async def getPassengerById(passenger_id: int) -> Passenger:
    passengers: list[Passenger] = list(
        filter(lambda p: p.id == passenger_id, passengers_db)
    )
    if len(passengers) == 0:
        raise HTTPException(
            status_code=404, detail=f"Passenger with id : '{passenger_id}' not found"
        )
    return passengers[0]


async def createPassenger(passenger: Passenger) -> Passenger:
    passenger.id = len(passengers_db) + 1
    new_passenger = Passenger.model_validate(passenger)
    passengers_db.append(new_passenger)
    return new_passenger


async def updatePassenger(passenger_id: int, passenger: Passenger) -> Passenger:
    existing_passenger = await getPassengerById(passenger_id)
    passenger_index = passengers_db.index(existing_passenger)
    passenger.id = existing_passenger.id
    passengers_db.remove(existing_passenger)
    passengers_db.insert(passenger_index, passenger)
    return passenger


async def deletePassenger(passenger: Passenger):
    # Mila fafana ihany koa ny booking
    passengers_db.remove(passenger)
