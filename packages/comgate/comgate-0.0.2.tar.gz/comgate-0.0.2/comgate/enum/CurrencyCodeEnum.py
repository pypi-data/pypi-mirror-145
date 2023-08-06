import enum


@enum.unique
class CurrencyCodeEnum(enum.Enum):
    CZK = 'CZK'
    EUR = 'EUR'
    PLN = 'PLN'
    HUF = 'HUF'
    USD = 'USD'
    GBP = 'GBP'
