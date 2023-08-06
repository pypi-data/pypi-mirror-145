from abc import abstractmethod, ABC
from typing import Tuple, Callable

from arrow_bpmn.__spi__ import Environment, State
from arrow_bpmn.__spi__.action import Actions
from arrow_bpmn.__spi__.execution.executable import Executable


class ServiceFactory(ABC):

    @abstractmethod
    def __call__(self, group: str, implementation: str) -> Executable:
        pass


class ServiceFactoryAware(ABC):

    @abstractmethod
    def with_service_factory(self, service_factory: ServiceFactory, environment: Environment):
        pass


class NoOpExecutable(Executable):

    def execute(self, state: State, environment: Environment) -> Tuple[State, Actions]:
        return state, []


class NoOpServiceFactory(ServiceFactory):

    def __call__(self, group: str, implementation: str) -> Executable:
        return NoOpExecutable()


class LambdaServiceFactory(ServiceFactory):

    def __init__(self, _callable: Callable[[str, str], Executable]):
        self.callable = _callable

    def __call__(self, group: str, implementation: str) -> Executable:
        return self.callable(group, implementation)
