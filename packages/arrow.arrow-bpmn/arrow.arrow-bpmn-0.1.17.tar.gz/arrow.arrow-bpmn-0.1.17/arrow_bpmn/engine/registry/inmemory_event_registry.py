from time import time
from typing import List, Dict, Optional, Union

from arrow_bpmn.__spi__.registry.event import Event
from arrow_bpmn.__spi__.registry.process_ref import ProcessRef
from arrow_bpmn.engine.registry.abstract_event_registry import EventRegistry, NodeRef, EventStr


class InMemoryEventRegistry(EventRegistry):
    """
    EventRegistry implementation which stores the events in an inmemory storage based on an event_source and an
    event_target dictionary.

    The event_sources dictionary maps an event_key to a map of node_key/timestamp mappings.
    The event_targets dictionary maps a node_key to a map of event_key/timestamp mappings.
    """

    def __init__(self):
        self.event_sources: Dict[str, Dict[str, float]] = {}
        self.event_targets: Dict[str, Dict[str, float]] = {}
        self.process_events: Dict[str, Dict[str, float]] = {}
        self.consumables: List[str] = []

    def create_subscription(self, event: Event, node_ref: NodeRef, consumable: bool):
        timestamp = time()
        event_key = str(event)
        node_key = str(node_ref)

        if event_key not in self.event_sources:
            self.event_sources[event_key] = {node_key: timestamp}
        else:
            self.event_sources[event_key][node_key] = timestamp

        if node_key not in self.event_targets:
            self.event_targets[node_key] = {event_key: timestamp}
        else:
            self.event_targets[node_key][event_key] = timestamp

        if consumable:
            self.consumables.append(str(node_ref))

        process_key = str(ProcessRef(node_ref.group, node_ref.process_id))
        if process_key not in self.process_events:
            self.process_events[process_key] = {}
        self.process_events[process_key][event_key] = timestamp

    def delete_subscription(self, event: Optional[Union[Event, EventStr]], node_ref: NodeRef):
        event_refs = []

        if event is None:
            if node_ref in self.event_targets:
                event_refs += self.event_targets[str(node_ref)].keys()
        else:
            event_refs += [str(event)]

        for event_ref in event_refs:
            del self.event_targets[str(node_ref)][event_ref]
            del self.event_sources[event_ref][str(node_ref)]

    def delete_subscriptions(self, process_ref: ProcessRef):
        event_refs = self.process_events[str(process_ref)].keys()

        for event_ref in event_refs:
            for node_ref in self.get_subscriptions(event_ref):
                self.delete_subscription(event_ref, node_ref)

    # TODO: sort by timestamps
    def get_subscriptions(self, event: Union[Event, EventStr]) -> List[NodeRef]:
        node_refs = []

        if str(event) in self.event_sources:
            for node_ref in self.event_sources[str(event)]:
                node_refs.append(NodeRef.parse(node_ref))

        for node_ref in node_refs:
            if node_ref in self.consumables:
                self.delete_subscription(event, node_ref)
                self.consumables.remove(node_ref)

        return node_refs
