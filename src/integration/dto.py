from datetime import datetime

from openai import BaseModel


class BookingWindow(BaseModel):
    start_date_time: datetime
    end_date_time: datetime


class Booking(BaseModel):
    booking_id: str
    address: str
    hotel_name: str
    room_number: str
    window: BookingWindow
    total_sla: int
    status: str


class BookingChangeResponse(BaseModel):
    success: bool
    reason: str | None = None
    updated_booking: Booking | None = None
