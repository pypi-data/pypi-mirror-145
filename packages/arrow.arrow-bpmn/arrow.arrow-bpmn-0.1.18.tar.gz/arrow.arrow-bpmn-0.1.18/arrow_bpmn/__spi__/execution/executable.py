from abc import ABC, abstractmethod
from typing import Tuple

from arrow_bpmn.__spi__ import State, Environment
from arrow_bpmn.__spi__.action import Actions


class Executable(ABC):

    @abstractmethod
    def execute(self, state: State, environment: Environment) -> Tuple[State, Actions]:
        pass
