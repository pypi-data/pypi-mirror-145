from abc import abstractmethod, ABC

from arrow_dmn.__spi__.dmn_engine import DmnEngine


class BusinessRuleFactory(ABC):

    @abstractmethod
    def __call__(self, group: str, implementation: str) -> DmnEngine:
        pass
