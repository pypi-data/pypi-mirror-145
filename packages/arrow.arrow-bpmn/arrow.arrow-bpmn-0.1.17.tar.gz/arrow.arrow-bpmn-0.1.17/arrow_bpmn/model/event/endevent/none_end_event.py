from typing import Tuple

from arrow_bpmn.__spi__ import BpmnNode
from arrow_bpmn.__spi__ import CompleteAction
from arrow_bpmn.__spi__.action import Actions
from arrow_bpmn.__spi__.execution import Environment
from arrow_bpmn.__spi__.execution import State


class NoneEndEvent(BpmnNode):
    """
    Default BPMN end event implementation. This element completes a process run
    and invokes the BPMN engine to store the process state.

    The xml representation of this node is
    <bpmn:endEvent />
    """

    def __init__(self, element: dict):
        super().__init__(element)

    def execute(self, state: State, environment: Environment) -> Tuple[State, Actions]:
        return state, [CompleteAction(self.id, consume_token=True)]

    def __repr__(self):
        return f"NoneEndEvent({self.id})"