from typing import Tuple

from arrow_bpmn.__spi__ import BpmnNode
from arrow_bpmn.__spi__ import CompleteAction
from arrow_bpmn.__spi__.action import ContinueAction, Actions, QueueAction
from arrow_bpmn.__spi__.execution import Environment
from arrow_bpmn.__spi__.execution import State
from arrow_bpmn.engine.registry.abstract_event_registry import ManualEvent


class ManualTask(BpmnNode):
    """
    A Manual Task defines a task that is external to the BPM engine. It is used to model work that is done by somebody
    who the engine does not need to know of and that has no known system or UI interface. For the engine, a manual task
    is handled as a pass-through activity, automatically continuing the process when the process execution arrives at it.
    """

    def __init__(self, element: dict):
        super().__init__(element)

    # noinspection PyBroadException
    def execute(self, state: State, environment: Environment) -> Tuple[State, Actions]:
        if state.is_reentry:
            actions = [ContinueAction(node) for node in environment.get_outgoing_nodes(self.id)]
            return state, [CompleteAction(self.id)] + actions

        event = ManualEvent(environment.group, environment.process_id, self.id, {})
        return state, [QueueAction(self.id, event=event, save_state=True)]

    def __repr__(self):
        return f"ManualTask({self.id})"
