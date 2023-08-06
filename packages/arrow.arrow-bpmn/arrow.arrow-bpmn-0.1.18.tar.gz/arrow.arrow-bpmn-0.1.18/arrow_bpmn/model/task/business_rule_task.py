from typing import Tuple

from arrow_bpmn.__spi__ import BpmnNode, CompleteAction
from arrow_bpmn.__spi__.action import Actions, ContinueAction
from arrow_bpmn.__spi__.execution import Environment
from arrow_bpmn.__spi__.execution import State
from arrow_bpmn.__spi__.factory.business_rule_factory import BusinessRuleFactory
from arrow_bpmn.__spi__.registry.process_ref import ProcessRef


class BusinessRuleTask(BpmnNode):

    @property
    def implementation(self):
        return self._get_property("implementation")

    def with_business_rule_factory(self, factory: BusinessRuleFactory, environment: Environment):
        if isinstance(self.implementation, str):
            self.__dict__["implementation"] = factory(environment.group, self.implementation)

    def execute(self, state: State, environment: Environment) -> Tuple[State, Actions]:
        engine = environment.business_rule_factory(self.implementation)
        process_ref = ProcessRef(environment.group, self.implementation)
        state.properties.update(engine.execute(process_ref, state.properties))

        actions = [ContinueAction(node) for node in environment.get_outgoing_nodes(self.id)]
        return state, [CompleteAction(self.id)] + actions

    def __repr__(self):
        return f"BusinessRuleTask({self.id})"
