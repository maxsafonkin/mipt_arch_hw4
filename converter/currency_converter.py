from . import structures as struct
from .errors_handler import handle_rates_provider_error
from .rates_provider import RatesProviderInterface


class CurrencyConverter:
    def __init__(self, rates_provider: RatesProviderInterface) -> None:
        self._rates_provider = rates_provider

    @handle_rates_provider_error
    def convert(self, amount: float, currency: struct.Currency) -> float:
        rate = self._rates_provider.get_rate(currency)
        return amount * rate
