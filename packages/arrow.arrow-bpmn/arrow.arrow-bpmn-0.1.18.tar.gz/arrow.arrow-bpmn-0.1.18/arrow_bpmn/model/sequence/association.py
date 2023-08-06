from arrow_bpmn.__spi__ import BpmnEdge


class Association(BpmnEdge):

    def __init__(self, attributes: dict):
        super().__init__(attributes)

    @property
    def association_direction(self) -> str:
        return self.__dict__["associationDirection"]

    @property
    def source_ref(self) -> str:
        return self.__dict__["sourceRef"]

    @property
    def target_ref(self) -> str:
        return self.__dict__["targetRef"]
