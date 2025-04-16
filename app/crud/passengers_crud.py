from app.models.passenger_model import Passenger
from ..db.fake_db import passengers_db


async def getAllPassengers() -> list[Passenger] | None:
    if len(passengers_db) == 0:
        return None
    return passengers_db


async def getPassengerById(passenger_id: int) -> Passenger | None:
    passengers: list[Passenger] = list(
        filter(lambda p: p.id == passenger_id, passengers_db)
    )
    if len(passengers) != 0:
        return passengers[0]
    return None


async def deletePassenger(passenger: Passenger):
    passengers_db.remove(passenger)
