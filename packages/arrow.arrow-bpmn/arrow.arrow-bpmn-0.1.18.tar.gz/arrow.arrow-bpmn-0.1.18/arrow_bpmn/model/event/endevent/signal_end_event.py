from typing import Tuple

from arrow_bpmn.__spi__.action import Actions
from arrow_bpmn.__spi__.action.event_action import EventAction
from arrow_bpmn.__spi__.execution import Environment
from arrow_bpmn.__spi__.execution import State
from arrow_bpmn.engine.registry.abstract_event_registry import SignalEvent
from arrow_bpmn.model.event.endevent.none_end_event import NoneEndEvent


class SignalEndEvent(NoneEndEvent):
    """
    When process execution arrives at a Signal End Event, the current path of execution is ended and a signal is sent.
    """

    def __init__(self, element: dict, signal: str):
        super().__init__(element)
        self.signal = signal

    def execute(self, state: State, environment: Environment) -> Tuple[State, Actions]:
        actions = super().execute(state, environment)
        return state, [EventAction(self.id, SignalEvent(environment.group, self.signal))] + actions

    def __repr__(self):
        return f"SignalEndEvent({self.id})"
