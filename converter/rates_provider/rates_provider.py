import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import requests

from .. import structures as struct
from .config import RatesProviderConfig
from .errors import RatesFetchingError
from .interface import RatesProviderInterface


@dataclass
class RatesCache:
    rates: dict[struct.Currency, struct.Rate]
    updated_at: datetime

    def is_expired(self, cache_expiry: int) -> bool:
        return self.updated_at < datetime.now(timezone.utc) - timedelta(seconds=cache_expiry)


class RatesProvider(RatesProviderInterface):
    def __init__(self, config: RatesProviderConfig) -> None:
        self._config = config
        self._rates = self._fetch_rates()

    def get_rate(self, currency: struct.Currency) -> float:
        if self._rates.is_expired(self._config.cache_expiry):
            self._rates = self._fetch_rates()
        return self._rates.rates[currency].value

    def _fetch_rates(self) -> RatesCache:
        rates_response = self._send_rate_request()
        rates = self._extract_rates(rates_response)
        return RatesCache(rates=rates, updated_at=datetime.now(timezone.utc))

    def _send_rate_request(self) -> requests.Response:
        # TODO: implement a separate module `API` for encapsulating logic
        # related to sending requests and handling errors
        for _ in range(self._config.max_retries):
            try:
                response = requests.get(self._config.url, timeout=self._config.timeout)
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as exc:
                if _ == self._config.max_retries - 1:
                    msg_exc = (
                        f"Не удалось выполнить запрос курсов конвертации после "
                        f"{self._config.max_retries} попыток: {exc}"
                    )
                    raise RatesFetchingError(msg_exc) from exc
                time.sleep(self._config.retry_delay)

        msg_exc = "Не удалось выполнить запрос курсов конвертации после всех попыток"
        raise RatesFetchingError(msg_exc)

    def _extract_rates(self, rates_response: requests.Response) -> dict[struct.Currency, struct.Rate]:
        try:
            rates_data = rates_response.json()
        except (requests.JSONDecodeError, KeyError) as exc:
            msg_exc = f"Не удалось извлечь курсы конвертации из ответа: {exc}"
            raise RatesFetchingError(msg_exc) from exc

        rates = {
            struct.Currency(currency_code): struct.Rate(currency=struct.Currency(currency_code), value=rate_value)
            for currency_code, rate_value in rates_data["rates"].items()
            if currency_code in struct.Currency._value2member_map_
        }
        return rates
