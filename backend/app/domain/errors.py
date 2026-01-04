class DomainError(Exception):
    ...


class SeatNotAvailable(DomainError):
    ...


class HoldExpired(DomainError):
    ...


class BookingNotFound(DomainError):
    ...


class PaymentFailed(DomainError):
    ...
