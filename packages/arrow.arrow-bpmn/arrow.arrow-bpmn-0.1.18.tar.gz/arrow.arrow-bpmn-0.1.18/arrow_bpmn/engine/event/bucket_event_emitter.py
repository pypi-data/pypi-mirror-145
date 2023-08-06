from arrow_bpmn.__spi__.action import Actions
from arrow_bpmn.__spi__.execution.event_emitter import EventEmitter
from arrow_bpmn.__spi__.registry.event import Event
from arrow_bpmn.engine.registry.abstract_event_registry import EventRegistry


class BucketEventEmitter(EventEmitter):
    def __init__(self):
        self.bucket = []

    def emit(self, event: Event, event_registry: EventRegistry) -> Actions:
        self.bucket += [event]
        return []
