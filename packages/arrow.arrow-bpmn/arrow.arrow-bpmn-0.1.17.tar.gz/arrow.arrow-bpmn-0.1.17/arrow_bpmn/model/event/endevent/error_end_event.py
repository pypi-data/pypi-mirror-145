from typing import Tuple

from arrow_bpmn.__spi__.action import Actions
from arrow_bpmn.__spi__.action.event_action import EventAction
from arrow_bpmn.__spi__.execution import Environment
from arrow_bpmn.__spi__.execution import State
from arrow_bpmn.engine.registry.abstract_event_registry import ErrorEvent
from arrow_bpmn.model.event.endevent.none_end_event import NoneEndEvent


class ErrorEndEvent(NoneEndEvent):
    """
    When process execution arrives at a Signal End Event, the current path of execution is ended and an error is sent.
    """

    def __init__(self, element: dict, error: str):
        super().__init__(element)
        self.error = error

    def execute(self, state: State, environment: Environment) -> Tuple[State, Actions]:
        actions = super().execute(state, environment)
        return state, [EventAction(self.id, ErrorEvent(environment.group, self.error))] + actions

    def __repr__(self):
        return f"SignalEndEvent({self.id})"
