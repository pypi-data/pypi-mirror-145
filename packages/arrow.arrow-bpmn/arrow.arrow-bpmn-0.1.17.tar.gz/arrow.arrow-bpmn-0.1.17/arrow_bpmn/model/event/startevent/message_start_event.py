from arrow_bpmn.__spi__ import NodeRef
from arrow_bpmn.engine.registry.abstract_event_registry import EventRegistryAware, EventRegistry, MessageEvent, \
    ProcessRef
from arrow_bpmn.model.event.startevent.none_start_event import NoneStartEvent


class MessageStartEvent(NoneStartEvent, EventRegistryAware):
    """
    A process can have one or more message start events (besides other types of start events).
    Each of the message events must have a unique message name.

    When a process is deployed then it creates a message subscription for each message start event.
    Message subscriptions of the previous version of the process (based on the BPMN process id) are closed.

    When the message subscription is created then a message can be correlated to the start event if the message name
    matches. On correlating the message, a new process instance is created and the corresponding message start event is
    activated.

    Messages are not correlated if they were published before the process was deployed. Or, if a new version of the
    process is deployed which doesn't have a proper start event.

    The correlationKey of a published message can be used to control the process instance creation.
    If an instance of this process is active (independently from its version) and it was triggered by a message with
    the same correlationKey then the message is not correlated and no new instance is created. When the active process
    instance is ended (completed or terminated) and a message with the same correlationKey and a matching message name
    is buffered (i.e. TTL > 0) then this message is correlated and a new instance of the latest version of the process
    is created.

    If the correlationKey of a message is empty then it will always create a new process instance and does not check if
    an instance is already active.
    """

    def __init__(self, attributes: dict, message: str):
        super().__init__(attributes)
        self.message = message

    def with_event_registry(self, process_ref: ProcessRef, event_registry: EventRegistry):
        event = MessageEvent(process_ref.group, self.message)
        event_registry.create_subscription(event, NodeRef(process_ref.group, process_ref.process_id, self.id), False)

    def __repr__(self):
        return f"MessageStartEvent({self.id})"
