import enum


@enum.unique
class PaymentStatusCodeEnum(enum.Enum):
    PENDING = 'PENDING'
    PAID = 'PAID'
    CANCELED = 'CANCELLED'
    AUTHORIZED = 'AUTHORIZED'
