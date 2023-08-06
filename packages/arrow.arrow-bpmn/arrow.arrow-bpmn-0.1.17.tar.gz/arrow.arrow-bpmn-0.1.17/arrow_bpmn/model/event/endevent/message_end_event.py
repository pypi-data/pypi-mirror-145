from typing import Tuple

from arrow_bpmn.__spi__.action import Actions
from arrow_bpmn.__spi__.action.event_action import EventAction
from arrow_bpmn.__spi__.execution import Environment
from arrow_bpmn.__spi__.execution import State
from arrow_bpmn.engine.registry.abstract_event_registry import MessageEvent
from arrow_bpmn.model.event.endevent.none_end_event import NoneEndEvent


class MessageEndEvent(NoneEndEvent):
    """
    When process execution arrives at a Message End Event, the current path of execution is ended and a message is sent.
    """

    def __init__(self, element: dict, message: str):
        super().__init__(element)
        self.message = message

    def execute(self, state: State, environment: Environment) -> Tuple[State, Actions]:
        actions = super().execute(state, environment)
        return state, [EventAction(self.id, MessageEvent(environment.group, self.message))] + actions

    def __repr__(self):
        return f"MessageEndEvent({self.id})"
