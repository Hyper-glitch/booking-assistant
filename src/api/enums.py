from enum import StrEnum


class Channel(StrEnum):
    WEB = "WEB"
    MOBILE = "MOBILE"
    API = "API"


class BookingDecision(StrEnum):
    TO_OPERATOR = "TO_OPERATOR"
    LEAVE_INITIAL = "LEAVE_INITIAL"
    CONFIRM_CHANGING = "CONFIRM_CHANGING"
    REJECT_CHANGING = "REJECT_CHANGING"
