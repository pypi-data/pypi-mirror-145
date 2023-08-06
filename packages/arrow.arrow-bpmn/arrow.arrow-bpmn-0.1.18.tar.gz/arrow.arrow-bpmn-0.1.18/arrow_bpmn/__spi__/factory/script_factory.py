from abc import ABC, abstractmethod
from typing import Callable, Optional, Any

from scriptable.api.property_resolver import PropertySource

from arrow_bpmn.__spi__ import State

Script = Callable[[Optional[PropertySource]], Any]


class ScriptFactory(ABC):

    @abstractmethod
    def __call__(self, state: State, language: str, script: str) -> Script:
        pass
