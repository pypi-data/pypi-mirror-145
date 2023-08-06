from abc import ABC, abstractmethod
from typing import Tuple, Optional

from arrow_bpmn.__spi__.action import Actions
from arrow_bpmn.__spi__.execution import State, Environment
from arrow_bpmn.parser.xml.xml_element import XMLElement


class BpmnNode(ABC):

    def __init__(self, element: dict):
        self.__dict__ = element.get_attributes() if isinstance(element, XMLElement) else element

    @property
    def name(self) -> str:
        """
        Returns the name of the edge.
        :return: str
        """
        return self._get_property("name")

    @property
    def id(self) -> str:
        """
        Returns the id of the edge.
        :return: str
        """
        return self._get_property("id")

    @abstractmethod
    def execute(self, state: State, environment: Environment) -> Tuple[State, Actions]:
        pass

    @abstractmethod
    def __repr__(self):
        pass

    def _get_property(self, key: str) -> Optional[str]:
        return self.__dict__[key] if key in self.__dict__ else None

    def __getitem__(self, item):
        return self.__dict__[item] if item in self.__dict__ else None
