from typing import Annotated
from fastapi import APIRouter, Path, Query, status


from app.models.booking_model import Booking, BookingRequest
from app.services.booking_service import (
    bookingFlight,
    getAllBookings,
    getBookingById,
    getBookingsFlight,
    getPassengerBookings,
    updateBooking,
)


router = APIRouter(prefix="/bookins", tags=["Booking Flight"])


@router.get("/", response_model=False)
async def get_all_bookings() -> list[Booking] | dict:
    bookins = await getAllBookings()
    if bookins:
        return bookins
    return {"message": "Bookins still empty."}


@router.get("/{booking_id}")
async def get_booking_by_id(booking_id: Annotated[int, Path(gt=0)]) -> Booking:
    booking = await getBookingById(booking_id)
    return booking


@router.get("/passenger/{passenger_id}", response_model=False)
async def get_passenger_bookins(
    passenger_id: Annotated[int, Path(gt=0)],
) -> list[Booking] | dict:
    bookings = await getPassengerBookings(passenger_id)
    if bookings:
        return bookings
    return {"message": "No booking made by this passenger."}


@router.get("/flight/{flight_id}", response_model=False)
async def get_bookings_flight(
    flight_id: Annotated[int, Path(gt=0)],
) -> list[Booking] | dict:
    bookings = await getBookingsFlight(flight_id)
    if bookings:
        return bookings
    return {"message": "No booking made with this flight."}


@router.put("/{booking_id}")
async def update_booking(
    booking_id: Annotated[int, Path(gt=0)], booking_request: BookingRequest
) -> Booking:
    updated_booking = await updateBooking(booking_id, booking_request)
    return updated_booking


@router.post("/", status_code=status.HTTP_201_CREATED)
async def booking_flight(
    passenger_id: Annotated[int, Query(gt=0)],
    flight_id: Annotated[int, Query(gt=0)],
    booking_request: BookingRequest,
) -> Booking:
    booking = await bookingFlight(passenger_id, flight_id, booking_request)
    return booking
