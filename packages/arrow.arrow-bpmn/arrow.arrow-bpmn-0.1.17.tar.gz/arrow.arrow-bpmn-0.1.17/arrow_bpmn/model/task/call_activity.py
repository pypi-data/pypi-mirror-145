from dataclasses import dataclass
from typing import List, Tuple

from scriptable.typescript_engine import TypescriptEngine

from arrow_bpmn.__spi__ import BpmnNode
from arrow_bpmn.__spi__ import CompleteAction
from arrow_bpmn.__spi__.action import ContinueAction, Actions
from arrow_bpmn.__spi__.action.cascade_action import CascadeAction
from arrow_bpmn.__spi__.action.queue_action import QueueAction
from arrow_bpmn.__spi__.execution import Environment
from arrow_bpmn.__spi__.execution import State
from arrow_bpmn.__spi__.registry.node_ref import NodeRef


@dataclass
class StateMapping:
    source: str
    target: str


@dataclass
class VariableMapping(StateMapping):
    pass


@dataclass
class ExpressionMapping(StateMapping):
    pass


class CallActivity(BpmnNode):
    """
    BPMN 2.0 makes a distinction between an embedded subprocess and a call activity.
    From a conceptual point of view, both will call a subprocess when process execution arrives at the activity.

    The difference is that the call activity references a process that is external to the process definition, whereas
    the subprocess is embedded within the original process definition. The main use case for the call activity is to
    have a reusable process definition that can be called from multiple other process definitions.

    When process execution arrives at the call activity, a new process instance is created, which is used to execute the
    subprocess, potentially creating parallel child executions as within a regular process. The main process instance
    waits until the subprocess is completely ended, and continues the original process afterwards.
    """

    def __init__(self, attributes: dict, incoming_state: List[StateMapping], outgoing_state: List[StateMapping]):
        super().__init__(attributes)
        self.incoming_state = incoming_state
        self.outgoing_state = outgoing_state

    @property
    def called_element(self):
        return self.__dict__["calledElement"]

    def execute(self, state: State, environment: Environment) -> Tuple[State, Actions]:
        def map_state(mappings: List[StateMapping]):
            new_state = {}
            for mapping in mappings:
                if isinstance(mapping, VariableMapping):
                    new_state[mapping.target] = state[mapping.source]
                if isinstance(mapping, ExpressionMapping):
                    new_state[mapping.target] = TypescriptEngine.parse(mapping.source).execute(state.properties)
            return new_state

        if state.is_reentry:
            outgoing_state = map_state(self.outgoing_state)
            state.properties.update(outgoing_state)

            actions = [ContinueAction(node) for node in environment.get_outgoing_nodes(self.id)]
            return state, [CompleteAction(self.id)] + actions

        incoming_state = map_state(self.incoming_state)
        task_reference = NodeRef(environment.group, state.node_ref.process_id, self.id)

        return state, [
            QueueAction(self.id, save_state=False),
            CascadeAction(task_reference, self.called_element, incoming_state)
        ]

    def __repr__(self):
        return f"CallActivity({self.id})"
