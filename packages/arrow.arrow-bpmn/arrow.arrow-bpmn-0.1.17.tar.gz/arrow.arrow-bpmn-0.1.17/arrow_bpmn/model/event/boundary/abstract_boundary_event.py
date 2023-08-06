from arrow_bpmn.__spi__ import BpmnNode
from arrow_bpmn.parser.xml.xml_element import XMLElement


# noinspection PyAbstractClass
class BoundaryEvent(BpmnNode):

    def __init__(self, element: XMLElement):
        super().__init__(element)

    @property
    def attached_to_ref(self) -> str:
        """
        Returns the id of the attached node.
        :return: str
        """
        return self.__dict__["attachedToRef"]
