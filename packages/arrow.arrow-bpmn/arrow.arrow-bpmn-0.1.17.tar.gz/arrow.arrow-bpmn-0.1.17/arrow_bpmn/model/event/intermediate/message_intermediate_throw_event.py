from typing import Tuple

from arrow_bpmn.__spi__ import BpmnNode, CompleteAction
from arrow_bpmn.__spi__.action import Actions, ContinueAction
from arrow_bpmn.__spi__.action.event_action import EventAction
from arrow_bpmn.__spi__.execution import Environment
from arrow_bpmn.__spi__.execution import State
from arrow_bpmn.engine.registry.abstract_event_registry import MessageEvent


class MessageIntermediateThrowEvent(BpmnNode):
    """
    A Message Intermediate Throwing event sends a message to an external service.
    """

    def __init__(self, element: dict, message: str):
        super().__init__(element)
        self.message = message

    def execute(self, state: State, environment: Environment) -> Tuple[State, Actions]:
        actions = [ContinueAction(node) for node in environment.get_outgoing_nodes(self.id)]
        return state, [EventAction(self.id, MessageEvent(self.id, self.message)), CompleteAction(self.id)] + actions

    def __repr__(self):
        return f"MessageIntermediateThrowEvent({self.id})"
