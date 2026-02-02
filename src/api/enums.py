from enum import StrEnum


class Channel(StrEnum):
    WEB = "WEB"
    MOBILE = "MOBILE"
    API = "API"


class BookingDecision(StrEnum):
    PENDING = "PENDING"
    TO_OPERATOR = "TO_OPERATOR"
    LEAVE_INITIAL = "LEAVE_INITIAL"
    CONFIRM = "CONFIRM"
    REJECT = "REJECT"
