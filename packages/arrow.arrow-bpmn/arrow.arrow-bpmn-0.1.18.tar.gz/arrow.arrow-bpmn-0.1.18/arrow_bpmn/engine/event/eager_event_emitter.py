from arrow_bpmn.__spi__.action import Actions, ResumeAction
from arrow_bpmn.__spi__.execution.event_emitter import EventEmitter
from arrow_bpmn.__spi__.registry.event import Event
from arrow_bpmn.engine.registry.abstract_event_registry import EventRegistry


class EagerEventEmitter(EventEmitter):

    def emit(self, event: Event, event_registry: EventRegistry) -> Actions:
        subscriptions = event_registry.get_subscriptions(event)
        return [ResumeAction(node_ref) for node_ref in subscriptions]
