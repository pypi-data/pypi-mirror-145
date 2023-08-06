from abc import ABC

from arrow_bpmn.__spi__ import State, Environment
from arrow_bpmn.__spi__.action import Action
from arrow_bpmn.__spi__.bpmn_node import BpmnNode


class BpmnEngineListener(ABC):

    def on_action(self, action: Action, state: State, env: Environment):
        pass

    def before_node_execution(self, node: BpmnNode, state: State):
        pass

    def after_node_execution(self, node: BpmnNode, state: State):
        pass
