from dataclasses import dataclass
from enum import StrEnum


class Currency(StrEnum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    RUB = "RUB"
    CNY = "CNY"


@dataclass
class Rate:
    currency: Currency
    value: float
