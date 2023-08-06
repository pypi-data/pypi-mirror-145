from dataclasses import dataclass

from arrow_bpmn.__spi__.action import Action


@dataclass
class ContinueAction(Action):
    id: str
