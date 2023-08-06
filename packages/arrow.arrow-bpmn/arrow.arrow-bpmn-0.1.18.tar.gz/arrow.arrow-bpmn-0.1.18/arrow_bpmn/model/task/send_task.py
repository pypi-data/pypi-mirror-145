from typing import Tuple

from arrow_bpmn.__spi__ import BpmnNode
from arrow_bpmn.__spi__ import CompleteAction
from arrow_bpmn.__spi__.action import ContinueAction, Actions, EventAction
from arrow_bpmn.__spi__.execution import Environment
from arrow_bpmn.__spi__.execution import State
from arrow_bpmn.engine.registry.abstract_event_registry import MessageEvent


class SendTask(BpmnNode):
    """
    A Send Task is used to send a message.
    """

    @property
    def message_ref(self):
        return self.__dict__["messageRef"]

    def execute(self, state: State, environment: Environment) -> Tuple[State, Actions]:
        event = MessageEvent(self.id, environment.get_message(self.message_ref))

        actions = [ContinueAction(node) for node in environment.get_outgoing_nodes(self.id)]
        return state, [EventAction(self.id, event), CompleteAction(self.id)] + actions

    def __repr__(self):
        return f"SendTask({self.id})"
