from dataclasses import dataclass

from arrow_bpmn.__spi__.action import Action
from arrow_bpmn.__spi__.registry.event import Event


@dataclass
class EventAction(Action):
    id: str
    event: Event
