from typing import Tuple

from arrow_bpmn.__spi__ import CompleteAction
from arrow_bpmn.__spi__.action import Actions, ContinueAction, QueueAction
from arrow_bpmn.__spi__.execution import Environment
from arrow_bpmn.__spi__.execution import State
from arrow_bpmn.engine.registry.abstract_event_registry import MessageEvent
from arrow_bpmn.model.event.boundary.abstract_boundary_event import BoundaryEvent
from arrow_bpmn.parser.xml.xml_element import XMLElement


class MessageBoundaryEvent(BoundaryEvent):
    """
    Boundary events are catching events that are attached to an activity. This means that while the activity is running,
    the message boundary event is listening for named message. When this is caught, two things might happen, depending
    on the configuration of the boundary event:

    Interrupting boundary event: The activity is interrupted and the sequence flow going out of the event is followed.

    Non-interrupting boundary event: One token stays in the activity and an additional token is created which follows
    the sequence flow going out of the event.
    """

    def __init__(self, element: XMLElement, message: str):
        super().__init__(element)
        self.message = message

    def execute(self, state: State, environment: Environment) -> Tuple[State, Actions]:
        if state.is_reentry:
            actions = [ContinueAction(node) for node in environment.get_outgoing_nodes(self.id)]
            return state, [CompleteAction(self.id)] + actions

        return state, [QueueAction(self.id, event=MessageEvent(environment.group, self.message))]

    def __repr__(self):
        return f"MessageBoundaryEvent({self.id})"
