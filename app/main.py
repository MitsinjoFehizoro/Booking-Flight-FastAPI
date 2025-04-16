from fastapi import FastAPI

from .routers.passengers_router import router as passenger_router
from .routers.flights_router import router as flight_router

app = FastAPI(title="Booking Flight")

app.include_router(passenger_router)
app.include_router(flight_router)
