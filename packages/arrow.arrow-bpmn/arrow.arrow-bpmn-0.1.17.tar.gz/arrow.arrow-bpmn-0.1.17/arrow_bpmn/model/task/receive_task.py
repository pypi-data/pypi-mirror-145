from typing import Tuple

from arrow_bpmn.__spi__ import BpmnNode
from arrow_bpmn.__spi__ import CompleteAction
from arrow_bpmn.__spi__.action import ContinueAction, Actions, QueueAction
from arrow_bpmn.__spi__.execution import Environment
from arrow_bpmn.__spi__.execution import State
from arrow_bpmn.engine.registry.abstract_event_registry import MessageEvent


class ReceiveTask(BpmnNode):
    """
    A Receive Task is a simple task that waits for the arrival of a certain message. When the process execution arrives
    at a Receive Task, the process state is committed to the persistence storage. This means that the process will stay
    in this wait state until a specific message is received by the engine, which triggers continuation of the process
    beyond the Receive Task.
    """

    def __init__(self, element: dict):
        super().__init__(element)

    @property
    def message_ref(self):
        return self.__dict__["messageRef"]

    def execute(self, state: State, environment: Environment) -> Tuple[State, Actions]:
        if state.is_reentry:
            actions = [ContinueAction(node) for node in environment.get_outgoing_nodes(self.id)]
            return state, [CompleteAction(self.id)] + actions

        event = MessageEvent(environment.group, environment.get_message(self.message_ref))
        return state, [QueueAction(self.id, event=event, save_state=True)]

    def __repr__(self):
        return f"ReceiveTask({self.id})"
