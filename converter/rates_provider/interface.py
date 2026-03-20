import abc

from .. import structures as struct


class RatesProviderInterface(abc.ABC):
    @abc.abstractmethod
    def get_rate(self, currency: struct.Currency) -> float:
        pass
