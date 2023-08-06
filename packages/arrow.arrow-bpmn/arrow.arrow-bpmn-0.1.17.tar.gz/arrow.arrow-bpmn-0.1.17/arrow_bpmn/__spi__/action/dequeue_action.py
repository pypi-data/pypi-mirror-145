from dataclasses import dataclass
from typing import Optional

from arrow_bpmn.__spi__.action import Action
from arrow_bpmn.__spi__.registry.event import Event


@dataclass
class DequeueAction(Action):
    """
    This action implementation is used to remove the given event from the event registry.
    """

    id: str
    event: Optional[Event] = None
