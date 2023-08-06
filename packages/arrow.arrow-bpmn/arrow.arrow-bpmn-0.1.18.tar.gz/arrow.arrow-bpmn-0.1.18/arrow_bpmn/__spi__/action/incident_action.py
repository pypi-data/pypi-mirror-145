from dataclasses import dataclass
from typing import Optional

from arrow_bpmn.__spi__.action import Action


@dataclass
class IncidentAction(Action):
    id: str
    error_ref: str
    error_msg: Optional[str] = None
