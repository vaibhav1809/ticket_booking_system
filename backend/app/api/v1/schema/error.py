from pydantic import BaseModel


class TicketSystemError(BaseModel):
    code: str
    message: str
    request_id: str


class TicketSystemException(BaseException):
    message: str
