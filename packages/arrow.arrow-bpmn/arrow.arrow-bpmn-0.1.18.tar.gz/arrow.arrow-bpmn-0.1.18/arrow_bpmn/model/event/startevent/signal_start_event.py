from arrow_bpmn.__spi__ import NodeRef
from arrow_bpmn.engine.registry.abstract_event_registry import EventRegistryAware, EventRegistry, ProcessRef, \
    SignalEvent
from arrow_bpmn.model.event.startevent.none_start_event import NoneStartEvent


class SignalStartEvent(NoneStartEvent, EventRegistryAware):
    """
    A signal start event can be used to start a process instance using a named signal.

    When deploying a process definition with one or more signal start events, the following considerations apply:

    The name of the signal start event must be unique across a given process definition, i.e., a process definition must
    not have multiple signal start events with the same name. The engine throws an exception upon deployment of a
    process definition in case two or more signal start events reference the same signal or if two or more signal start
    events reference signals with the same signal name.

    Contrary to message start events, the name of the signal start event does not have to be unique across all deployed
    process definitions.

    Process versioning: Upon deployment of a new version of a process definition, the signal subscriptions of the
    previous version are canceled. This is also the case for signal events that are not present in the new version.

    A process instance of a process definition with one or more signal start events will be started, when a signal with
    the proper name is thrown.
    """

    def __init__(self, attributes: dict, signal: str):
        super().__init__(attributes)
        self.signal = signal

    def with_event_registry(self, process_ref: ProcessRef, event_registry: EventRegistry):
        event = SignalEvent(process_ref.group, self.signal)
        event_registry.create_subscription(event, NodeRef(process_ref.group, process_ref.process_id, self.id), False)

    def __repr__(self):
        return f"SignalStartEvent({self.id})"
