from pathlib import Path
from typing import Union, Optional

from arrow_bpmn.parser.xml.xml_element import XMLElement

BpmnSource = Union[Path, str, bytes]
Element = Union[XMLElement, dict]
OptDict = Optional[dict]