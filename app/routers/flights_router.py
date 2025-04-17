from operator import gt
from typing import Annotated
from fastapi import APIRouter, status, Path

from app.services.flights_service import (
    createFlight,
    deleteFlight,
    getAllFlights,
    getFlightById,
    updateFlight,
)
from app.models.flight_model import Flight


router = APIRouter(prefix="/flights", tags=["Flight"])


@router.get("/", response_model=False)
async def get_all_flight() -> list[Flight] | dict:
    flights = await getAllFlights()
    if flights:
        return flights
    return {"message": "Flights still empty"}


@router.get("/{flight_id}")
async def get_flight_by_id(flight_id: Annotated[int, Path(gt=0)]) -> Flight:
    flight = await getFlightById(flight_id)
    return flight


@router.put("/{flight_id}")
async def update_flight(
    flight_id: Annotated[int, Path(gt=0)], flight: Flight
) -> Flight:
    flight_updated = await updateFlight(flight_id, flight)
    return flight_updated


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_flight(flight: Flight) -> Flight:
    new_flight = await createFlight(flight)
    return new_flight


@router.delete("/{flight_id}")
async def delete_flight(flight_id: Annotated[int, Path(gt=0)]) -> Flight:
    flight = await getFlightById(flight_id)
    await deleteFlight(flight)
    return flight
