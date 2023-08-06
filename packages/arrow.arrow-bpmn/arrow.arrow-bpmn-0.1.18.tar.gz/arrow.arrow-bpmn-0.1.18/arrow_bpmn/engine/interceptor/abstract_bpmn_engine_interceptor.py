from abc import ABC

from arrow_bpmn.__spi__.bpmn_node import BpmnNode


# noinspection PyMethodMayBeStatic,PyUnusedLocal
class BpmnEngineInterceptor(ABC):

    def __call__(self, node: BpmnNode) -> BpmnNode:
        return node
