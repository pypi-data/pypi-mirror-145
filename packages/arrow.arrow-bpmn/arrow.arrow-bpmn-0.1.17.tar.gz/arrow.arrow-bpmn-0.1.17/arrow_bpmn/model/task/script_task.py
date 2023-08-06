from typing import Tuple

from arrow_bpmn.__spi__ import BpmnNode
from arrow_bpmn.__spi__ import CompleteAction
from arrow_bpmn.__spi__.action import ContinueAction, Actions, EventAction
from arrow_bpmn.__spi__.execution import Environment
from arrow_bpmn.__spi__.execution import State
from arrow_bpmn.engine.registry.abstract_event_registry import ErrorEvent


class ScriptTask(BpmnNode):

    @property
    def script_format(self):
        return self._get_property("scriptFormat")

    @property
    def script(self):
        return self._get_property("script")

    @property
    def var_name(self):
        return self._get_property("varName")

    # noinspection PyBroadException
    def execute(self, state: State, environment: Environment) -> Tuple[State, Actions]:
        try:
            engine = environment.script_factory(state, self.script_format, self.script)
            state[self.var_name] = engine(state.properties)
        except Exception:
            return state, [EventAction(self.id, ErrorEvent(environment.group, "script-error"))]

        actions = [ContinueAction(node) for node in environment.get_outgoing_nodes(self.id)]
        return state, [CompleteAction(self.id)] + actions

    def __repr__(self):
        return f"ScriptTask({self.id})"
