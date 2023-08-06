from typing import Tuple

from arrow_bpmn.__spi__ import BpmnNode, CompleteAction
from arrow_bpmn.__spi__.action import Actions, ContinueAction, QueueAction
from arrow_bpmn.__spi__.execution import Environment
from arrow_bpmn.__spi__.execution import State
from arrow_bpmn.engine.registry.abstract_event_registry import SignalEvent


class SignalIntermediateCatchEvent(BpmnNode):
    """
    When a token arrives at the signal intermediate catching event it will wait there until a signal with the proper
    name arrives.
    """

    def __init__(self, element: dict, signal: str):
        super().__init__(element)
        self.signal = signal

    def execute(self, state: State, environment: Environment) -> Tuple[State, Actions]:
        if state.is_reentry:
            actions = [ContinueAction(node) for node in environment.get_outgoing_nodes(self.id)]
            return state, [CompleteAction(self.id)] + actions

        return state, [QueueAction(self.id, event=SignalEvent(environment.group, self.signal), save_state=True)]

    def __repr__(self):
        return f"SignalIntermediateCatchEvent({self.id})"
