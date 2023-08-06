from dataclasses import dataclass

from arrow_bpmn.__spi__.action import Action
from arrow_bpmn.__spi__.registry.node_ref import NodeRef


@dataclass
class ResumeAction(Action):
    reference: NodeRef
