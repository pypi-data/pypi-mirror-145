from abc import ABC, abstractmethod

from arrow_bpmn.__spi__ import BpmnNode, BpmnEdge


class BpmnVisitor(ABC):

    @abstractmethod
    def visit_node(self, node: BpmnNode):
        pass

    def visit_edge(self, edge: BpmnEdge):
        pass
