from fastapi import HTTPException
from app.models.flight_model import Flight
from ..db.fake_db import flights_db


async def getAllFlights() -> list[Flight] | None:
    if len(flights_db) == 0:
        return None
    return flights_db


async def getFlightById(flight_id: int) -> Flight:
    flights: list[Flight] = list(filter(lambda f: f.id == flight_id, flights_db))
    if len(flights) == 0:
        raise HTTPException(
            status_code=404, detail=f"Flight with id : '{flight_id}' not found."
        )
    return flights[0]


async def createFlight(flight: Flight) -> Flight:
    flight.id = len(flights_db) + 1
    new_flight = Flight.model_validate(flight)
    flights_db.append(new_flight)
    return new_flight


async def deleteFlight(flight: Flight):
    flights_db.remove(flight)
