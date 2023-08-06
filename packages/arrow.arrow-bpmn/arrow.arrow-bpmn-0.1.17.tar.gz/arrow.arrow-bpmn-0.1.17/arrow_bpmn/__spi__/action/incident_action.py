from dataclasses import dataclass

from arrow_bpmn.__spi__.action import Action


@dataclass
class IncidentAction(Action):
    id: str
    error_ref: str
