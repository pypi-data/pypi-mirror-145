from typing import Tuple

from arrow_bpmn.__spi__ import CompleteAction
from arrow_bpmn.__spi__.action import Actions, ContinueAction, QueueAction
from arrow_bpmn.__spi__.execution import Environment
from arrow_bpmn.__spi__.execution import State
from arrow_bpmn.engine.registry.abstract_event_registry import ErrorEvent
from arrow_bpmn.model.event.boundary.abstract_boundary_event import BoundaryEvent


class ErrorBoundaryEvent(BoundaryEvent):
    """
    An intermediate catching error event on the boundary of an activity, or error boundary event for short, catches
    errors that are thrown within the scope of the activity on which it is defined.

    Defining a error boundary event makes most sense on an embedded subprocess, or a call activity, as a subprocess
    creates a scope for all activities inside the subprocess. Errors are thrown by error end events. Such an error will
    propagate its parent scopes upwards until a scope is found on which a error boundary event is defined that matches
    the error event definition.

    When an error event is caught, the activity on which the boundary event is defined is destroyed, also destroying all
    current executions therein (e.g., concurrent activities, nested subprocesses, etc.). Process execution continues
    following the outgoing sequence flow of the boundary event.

    A error boundary event is defined as a typical boundary event. As with the other error events, the errorRef
    references an error defined outside of the process element.

    The errorCode is used to match the errors that are caught:

    If errorRef is omitted, the error boundary event will catch any error event, regardless of the errorCode.
    Otherwise the boundary event will only catch errors with the defined error code.
    """

    def __init__(self, element: dict, error: str):
        super().__init__(element)
        self.error = error

    def execute(self, state: State, environment: Environment) -> Tuple[State, Actions]:
        if state.is_reentry:
            actions = [ContinueAction(node) for node in environment.get_outgoing_nodes(self.id)]
            return state, [CompleteAction(self.id)] + actions

        return state, [QueueAction(self.id, event=ErrorEvent(environment.group, self.error))]

    def __repr__(self):
        return f"ErrorBoundaryEvent({self.id})"