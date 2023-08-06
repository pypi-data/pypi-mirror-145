from abc import ABC, abstractmethod

from arrow_bpmn.__spi__.action import Actions
from arrow_bpmn.__spi__.registry.event import Event
from arrow_bpmn.engine.registry.abstract_event_registry import EventRegistry


class EventEmitter(ABC):

    @abstractmethod
    def emit(self, event: Event, event_registry: EventRegistry) -> Actions:
        pass
