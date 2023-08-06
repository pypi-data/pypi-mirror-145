from typing import Tuple

from arrow_bpmn.__spi__ import CompleteAction
from arrow_bpmn.__spi__.action import Actions, ContinueAction, QueueAction
from arrow_bpmn.__spi__.execution import Environment
from arrow_bpmn.__spi__.execution import State
from arrow_bpmn.engine.registry.abstract_event_registry import CompensationEvent
from arrow_bpmn.model.event.boundary.abstract_boundary_event import BoundaryEvent
from arrow_bpmn.parser.xml.xml_element import XMLElement


# TODO: handle <bpmn:association />
class CompensationBoundaryEvent(BoundaryEvent):
    """
    An attached intermediate catching compensation on the boundary of an activity, or, for short, a compensation
    boundary event, can be used to attach a compensation handler to an activity or an embedded subprocess.

    The compensation boundary event must reference a single compensation handler using a directed association.

    A compensation boundary event has a different activation policy than other boundary events. Other boundary events,
    such as the signal boundary event are activated when the activity they are attached to is started.
    When the activity is left, they are deactivated and the corresponding event subscription is canceled.
    The compensation boundary event is different. The compensation boundary is activated when the activity it is
    attached to completes successfully. At this point, the corresponding subscription to compensation events is created.
    The subscription is removed either when a compensation event is triggered or when the corresponding process instance
    ends. This leads to the following points:

    * When compensation is triggered, the compensation handler associated with the compensation boundary event is
    invoked the same amount of times that the activity it is attached to completed successfully.
    * If a compensation boundary event is attached to an activity with multiple instance characteristics, a compensation
    event subscription is created for each instance.
    * If a compensation boundary event is attached to an activity which is contained inside a loop, a compensation event
    subscription is created for each time the activity is executed.
    * If the process instance ends, the subscriptions to compensation events are canceled.
    """

    def __init__(self, element: XMLElement, message: str):
        super().__init__(element)
        self.message = message

    def execute(self, state: State, environment: Environment) -> Tuple[State, Actions]:
        if state.is_reentry:
            actions = [ContinueAction(node) for node in environment.get_outgoing_nodes(self.id)]
            return state, [CompleteAction(self.id)] + actions

        event = CompensationEvent(environment.group, state.node_ref.process_id, state.node_ref.process_instance_id)
        return state, [QueueAction(self.id, event=event)]

    def __repr__(self):
        return f"CompensationBoundaryEvent({self.id})"
