from typing import Tuple

from arrow_bpmn.__spi__ import BpmnNode
from arrow_bpmn.__spi__ import CompleteAction
from arrow_bpmn.__spi__ import NodeRef
from arrow_bpmn.__spi__.action import ContinueAction, Actions
from arrow_bpmn.__spi__.execution import Environment
from arrow_bpmn.__spi__.execution import State
from arrow_bpmn.engine.registry.abstract_event_registry import EventRegistryAware, ProcessRef, EventRegistry, \
    NoneEvent


class NoneStartEvent(BpmnNode, EventRegistryAware):

    def __init__(self, element: dict):
        super().__init__(element)

    def execute(self, state: State, environment: Environment) -> Tuple[State, Actions]:
        actions = [ContinueAction(node) for node in environment.get_outgoing_nodes(self.id)]
        return state, [CompleteAction(self.id)] + actions

    def with_event_registry(self, process_ref: ProcessRef, event_registry: EventRegistry):
        event = NoneEvent(process_ref.group, process_ref.process_id)
        event_registry.create_subscription(event, NodeRef(process_ref.group, process_ref.process_id, self.id), False)

    def __repr__(self):
        return f"NoneStartEvent({self.id})"
