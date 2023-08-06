from typing import Optional

from arrow_bpmn.__spi__ import BpmnEdge
from arrow_bpmn.parser.json.json_element import JSONElement
from arrow_bpmn.parser.xml.xml_element import XMLElement


class SequenceFlow(BpmnEdge):

    def __init__(self, attributes: dict, expression: Optional[str]):
        super().__init__(attributes)
        self.expression = expression

    @staticmethod
    def from_json(element: JSONElement) -> 'SequenceFlow':
        expression = element.pop("expression")
        return SequenceFlow(element.item, expression)

    @staticmethod
    def from_xml(element: XMLElement) -> 'SequenceFlow':
        if element.has_tag("bpmn:conditionExpression"):
            expression = element.get_tag("bpmn:conditionExpression")
            return SequenceFlow(element.get_attributes(), expression.get_text())
        return SequenceFlow(element.get_attributes(), None)
