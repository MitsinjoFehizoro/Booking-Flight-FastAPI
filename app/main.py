from fastapi import FastAPI

from .routers.passengers_router import router as passenger_router
from .routers.flights_router import router as flight_router
from .routers.bookins_router import router as booking_router

app = FastAPI(
    title="Booking Flight",
    description="Simple api for learn FastAPI",
    summary="Create a new flight and a new passenger, and book the flight for the passenger.",
    version="0.0.1",
    contact={"name": "Dagocloud", "email": "mitsinjo.ranaivoarisaona@dagocloud.com"},
)

app.include_router(passenger_router)
app.include_router(flight_router)
app.include_router(booking_router)
