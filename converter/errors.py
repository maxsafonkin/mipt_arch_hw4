class CurrencyConverterError(Exception):
    pass


class InvalidCurrencyError(CurrencyConverterError):
    pass


class UnableToFetchRatesError(CurrencyConverterError):
    pass
