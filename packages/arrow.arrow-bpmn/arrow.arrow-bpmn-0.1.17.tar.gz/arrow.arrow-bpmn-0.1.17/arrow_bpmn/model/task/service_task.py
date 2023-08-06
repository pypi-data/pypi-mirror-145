from typing import Tuple

from arrow_bpmn.__spi__ import BpmnNode
from arrow_bpmn.__spi__.action import Actions
from arrow_bpmn.__spi__.execution import Environment
from arrow_bpmn.__spi__.execution import State


class ServiceTask(BpmnNode):

    @property
    def implementation(self):
        return self.__dict__["implementation"]

    def execute(self, state: State, environment: Environment) -> Tuple[State, Actions]:
        delegate = environment.service_factory(environment.group, self.implementation)
        return delegate.execute(state, environment)

    def __repr__(self):
        return f"ServiceTask({self.id})"
