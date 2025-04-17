from fastapi import HTTPException
from pydantic import PositiveFloat

from app.models.flight_model import Flight
from app.models.passenger_model import Passenger
from app.services.flights_service import getFlightById
from app.services.passengers_service import getPassengerById
from ..db.fake_db import bookings_db, flights_db
from app.models.booking_model import Booking, BookingRequest


async def getAllBookings() -> list[Booking] | None:
    if len(bookings_db) == 0:
        return None
    return bookings_db


async def getBookingById(booking_id: int) -> Booking:
    bookings: list[Booking] = list(filter(lambda b: b.id == booking_id, bookings_db))
    if len(bookings) == 0:
        raise HTTPException(
            status_code=404,
            detail=f"Booking with id : '{booking_id}' not found",
        )
    return bookings[0]


async def getPassengerBookings(passenger_id: int) -> list[Booking] | None:
    bookings: list[Booking] = list(
        filter(lambda b: b.passenger.id == passenger_id, bookings_db)
    )
    if len(bookings) == 0:
        return None
    return bookings


async def getBookingsFlight(flight_id: int) -> list[Booking] | None:
    bookings: list[Booking] = list(
        filter(lambda b: b.flight.id == flight_id, bookings_db)
    )
    if len(bookings) == 0:
        return None
    return bookings


async def bookingFlight(
    passenger_id: int, flight_id: int, booking_request: BookingRequest
) -> Booking:
    passenger = await getPassengerById(passenger_id)
    flight = await getFlightById(flight_id)

    if (
        booking_request.place_number == 0
        or booking_request.place_number > flight.capacity
    ):
        raise HTTPException(
            status_code=400, detail=f"Place_number must be in 1 - {flight.capacity}"
        )
    if booking_request.place_number in flight.places_already_booked:
        raise HTTPException(
            status_code=400,
            detail=f"Place number '{booking_request.place_number}' already booked by other passenger.",
        )

    new_booking = Booking(
        passenger=passenger,
        flight=flight,
        travel_class=booking_request.travel_class,
        price=booking_request.price,
        place_number=booking_request.place_number,
    )
    flights_db[flight.id - 1].places_already_booked.add(new_booking.place_number)
    new_booking.id = len(bookings_db) + 1
    bookings_db.append(new_booking)
    return new_booking
