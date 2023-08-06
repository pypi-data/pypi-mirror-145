from arrow_bpmn.__spi__ import BpmnNode, State, Environment
from arrow_bpmn.__spi__.action import Action
from arrow_bpmn.engine.listener.abstract_bpmn_engine_listener import BpmnEngineListener


class CycleDetectionListener(BpmnEngineListener):

    def on_action(self, action: Action, state: State, env: Environment):
        super().on_action(action, state, env)

    def before_node_execution(self, node: BpmnNode, state: State):
        super().before_node_execution(node, state)

    def after_node_execution(self, node: BpmnNode, state: State):
        super().after_node_execution(node, state)