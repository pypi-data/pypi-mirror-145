from dataclasses import dataclass
from typing import Optional

from arrow_bpmn.__spi__.action import Action
from arrow_bpmn.__spi__.registry.event import Event


@dataclass
class QueueAction(Action):
    id: str
    save_state: bool = False
    event: Optional[Event] = None
    consumable: bool = True
