import typing as t

from . import errors as err
from .rates_provider import errors as rp_err


P = t.ParamSpec("P")
T = t.TypeVar("T")


def handle_rates_provider_error(func: t.Callable[P, T]) -> t.Callable[P, T]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        try:
            return func(*args, **kwargs)
        except rp_err.RatesProviderError as exc:
            msg_exc = f"Ошибка при получении курсов: {exc}"
            raise err.UnableToFetchRatesError(msg_exc) from exc

    return wrapper
