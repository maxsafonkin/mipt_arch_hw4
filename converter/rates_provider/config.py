from dataclasses import dataclass


@dataclass
class RatesProviderConfig:
    cache_expiry: int
    url: str
    max_retries: int
    retry_delay: int
    timeout: int
