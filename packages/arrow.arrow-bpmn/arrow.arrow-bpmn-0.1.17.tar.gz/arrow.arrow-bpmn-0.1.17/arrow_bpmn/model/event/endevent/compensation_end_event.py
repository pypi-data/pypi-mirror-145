from typing import Tuple

from arrow_bpmn.__spi__ import BpmnNode, State, Environment
from arrow_bpmn.__spi__.action import Actions, EventAction
from arrow_bpmn.engine.registry.abstract_event_registry import CompensationEvent


class CompensationEndEvent(BpmnNode):
    """
    A compensation end event triggers compensation and the current path of execution is ended. It has the same behavior
    and limitations as a compensation intermediate throwing event.
    """

    def __init__(self, attributes: dict):
        super().__init__(attributes)

    def execute(self, state: State, environment: Environment) -> Tuple[State, Actions]:
        actions = super().execute(state, environment)
        event = CompensationEvent(environment.group, state.node_ref.process_id, state.node_ref.process_instance_id)
        return state, [EventAction(self.id, event)] + actions

    def __repr__(self):
        return f"CompensationEndEvent({self.id})"
