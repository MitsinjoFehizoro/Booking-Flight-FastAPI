from fastapi import FastAPI

from .routers.passengers_router import router as passenger_router

app = FastAPI(title="Booking Flight")

app.include_router(passenger_router)
