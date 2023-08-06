from collections import UserDict
from typing import List

from arrow_bpmn.__spi__ import BpmnEdge
from arrow_bpmn.__spi__ import BpmnNode
from arrow_bpmn.__spi__.bpmn_visitor import BpmnVisitor
from arrow_bpmn.engine.registry.abstract_event_registry import EventRegistryAware, ProcessRef, EventRegistry
from arrow_bpmn.model.sequence.association import Association


class EventDict(UserDict):
    @property
    def messages(self):
        return self["message"]

    @property
    def signals(self):
        return self["signal"]

    @property
    def errors(self):
        return self["error"]


class Process(EventRegistryAware):

    def __init__(self,
                 attributes: dict,
                 sequence_flows: List[BpmnEdge],
                 associations: List[Association],
                 tasks: List[BpmnNode],
                 start_events: List[BpmnNode],
                 end_events: List[BpmnNode],
                 boundary_events: List[BpmnNode],
                 intermediate_events: List[BpmnNode],
                 gateways: List[BpmnNode],
                 events: EventDict):
        self.__dict__ = attributes
        self.sequence_flows = sequence_flows
        self.associations = associations
        self.tasks = tasks
        self.start_events = start_events
        self.end_events = end_events
        self.boundary_events = boundary_events
        self.intermediate_events = intermediate_events
        self.gateways = gateways
        self.events = events

    @property
    def id(self):
        return self.__dict__["id"]

    def with_event_registry(self, process_ref: ProcessRef, event_registry: EventRegistry):
        process_ref = ProcessRef(process_ref.group, self.id)

        for start_event in self.start_events:
            if isinstance(start_event, EventRegistryAware):
                start_event.with_event_registry(process_ref, event_registry)

    def to_json(self):
        import json
        return json.dumps(self._to_json(self))

    def _to_json(self, object) -> dict:
        obj = {}

        for k in (object.__dict__ if not isinstance(object, dict) else object):
            value = object.__dict__[k] if not isinstance(object, dict) else object[k]
            if type(value) == list:
                obj[k] = [{"type": type(x).__name__, "item": self._to_json(x)} for x in value]
            elif type(value) == dict:
                obj[k] = {"type": type(value).__name__}
                result = self._to_json(value)
                obj[k]["item"] = result["item"] if "item" in result else result
            elif isinstance(value, UserDict):
                obj[k] = {"type": type(value).__name__, "item": value.data}
            else:
                obj[k] = value

        return obj

    def accept(self, visitor: BpmnVisitor):
        [visitor.visit_node(node) for node in self.start_events]
        [visitor.visit_node(node) for node in self.end_events]
        [visitor.visit_node(node) for node in self.intermediate_events]
        [visitor.visit_node(node) for node in self.gateways]
        [visitor.visit_node(node) for node in self.boundary_events]
        [visitor.visit_node(node) for node in self.tasks]
        [visitor.visit_edge(edge) for edge in self.sequence_flows]
        [visitor.visit_edge(edge) for edge in self.associations]
