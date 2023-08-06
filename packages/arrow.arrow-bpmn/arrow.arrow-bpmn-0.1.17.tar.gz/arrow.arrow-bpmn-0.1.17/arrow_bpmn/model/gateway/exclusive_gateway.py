from typing import Tuple

from arrow_bpmn.__spi__ import BpmnNode
from arrow_bpmn.__spi__ import CompleteAction
from arrow_bpmn.__spi__.action import ContinueAction, Actions
from arrow_bpmn.__spi__.action.incident_action import IncidentAction
from arrow_bpmn.__spi__.execution import Environment
from arrow_bpmn.__spi__.execution import State


class ExclusiveGateway(BpmnNode):
    """
    An exclusive gateway (aka XOR-gateway) allows to make a decision based on data (i.e. on process instance variables).

    If an exclusive gateway has multiple outgoing sequence flows then all sequence flows, except one, must have a
    conditionExpression to define when the flow is taken. The gateway can have one sequence flow without
    conditionExpression which must be defined as the default flow.

    When an exclusive gateway is entered then the conditionExpressions are evaluated.
    The process instance takes the first sequence flow that condition is fulfilled.

    If no condition is fulfilled then it takes the default flow of the gateway.
    In case the gateway has no default flow, an incident is created.

    An exclusive gateway can also be used to join multiple incoming flows to one, in order to improve the readability
    of the BPMN. A joining gateway has a pass-through semantic. It doesn't merge the incoming concurrent flows like
    a parallel gateway.
    """

    def __init__(self, element: dict):
        super().__init__(element)

    @property
    def default(self):
        return self._get_property("default")

    def execute(self, state: State, environment: Environment) -> Tuple[State, Actions]:
        # try to find a sequence by expression
        # ************************************
        for edge in environment.get_outgoing_edges(self.id):
            if edge.expression is not None:
                engine = environment.script_factory(state, "typescript", edge.expression)
                if engine(state.properties):
                    return state, [CompleteAction(self.id), ContinueAction(edge.target_ref)]

        # try to find the default sequence
        # ********************************
        if self.default is not None:
            edge = environment.get_edge(self.default)
            if edge is None:
                return state, [IncidentAction(self.id, "not_continuable")]
            return state, [CompleteAction(self.id), ContinueAction(edge.target_ref)]

        return state, [IncidentAction(self.id, "not_continuable")]

    def __repr__(self):
        return f"ExclusiveGateway({self.id})"
