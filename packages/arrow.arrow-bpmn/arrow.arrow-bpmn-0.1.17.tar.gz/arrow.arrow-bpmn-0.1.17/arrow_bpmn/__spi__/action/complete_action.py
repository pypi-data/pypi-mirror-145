from dataclasses import dataclass

from arrow_bpmn.__spi__.action import Action


@dataclass
class CompleteAction(Action):
    id: str
    save_state: bool = False
    consume_token: bool = False
    product_token: bool = False
