from typing import Tuple

from arrow_bpmn.__spi__ import BpmnNode, State, Environment
from arrow_bpmn.__spi__.action import Actions
from arrow_bpmn.engine.interceptor.abstract_bpmn_engine_interceptor import BpmnEngineInterceptor


class ArrowExtensionInterceptor(BpmnEngineInterceptor):

    def __call__(self, node: BpmnNode) -> BpmnNode:
        if "Task" in type(node).__name__:
            return ExpressionTaskAdapter(node)
        return node


class ExpressionTaskAdapter(BpmnNode):
    """
    This adapter implementation adds the cross cutting concern of handling initiate, complete and continue expressions
    to a bpmn node.
    """

    def __init__(self, node: BpmnNode):
        super().__init__(node.__dict__)
        self.delegate = node

    def execute(self, state: State, environment: Environment) -> Tuple[State, Actions]:
        result = None

        if self.initiate_expression is not None:
            expr = environment.script_factory(state, self.initiate_expression_format, self.initiate_expression)
            result = expr(state.properties)
            if isinstance(result, dict):
                state.properties.update(result)
            elif result is not None:
                state.properties.update({"result": result})

        if self.continue_expression is not None:
            expr = environment.script_factory(state, self.continue_expression_format, self.continue_expression)
            # noinspection PySimplifyBooleanCheck
            if expr(state.properties) is True:
                result = self.delegate.execute(state.with_is_reentry(True), environment)

        if result is None:
            result = self.delegate.execute(state, environment)

        if self.complete_expression is not None:
            expr = environment.script_factory(state, self.complete_expression_format, self.complete_expression)
            _result = expr(state.properties)
            if isinstance(_result, dict):
                state.properties.update(_result)
            elif _result is not None:
                state.properties.update({"result": _result})

        return result

    @property
    def initiate_expression_format(self):
        return self.__dict__["initiateExpressionFormat"] if "initiateExpressionFormat" in self.__dict__ else "typescript"

    @property
    def initiate_expression(self):
        return self.__dict__["initiateExpression"] if "initiateExpression" in self.__dict__ else None

    @property
    def complete_expression_format(self):
        return self.__dict__["completeExpressionFormat"] if "completeExpressionFormat" in self.__dict__ else "typescript"

    @property
    def complete_expression(self):
        return self.__dict__["completeExpression"] if "completeExpression" in self.__dict__ else None

    @property
    def continue_expression_format(self):
        return self.__dict__["continueExpressionFormat"] if "continueExpressionFormat" in self.__dict__ else "typescript"

    @property
    def continue_expression(self):
        return self.__dict__["continueExpression"] if "continueExpression" in self.__dict__ else None

    def __repr__(self):
        return self.delegate.__repr__()
