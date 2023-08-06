from dataclasses import dataclass, field
from typing import Optional

from arrow_bpmn.__spi__.registry.node_ref import NodeRef


@dataclass
class State:
    """
    This class holds all relevant information about a bpmn process run.
    The variables are immutable.
    """
    properties: dict
    node_ref: NodeRef
    is_reentry: bool = False
    parent_reference: Optional[NodeRef] = None
    header: dict = field(default_factory=lambda: {})

    def with_is_reentry(self, is_reentry: bool):
        return State(self.properties, self.node_ref, is_reentry, self.parent_reference, self.header)

    def with_parent_reference(self, parent_reference: Optional[NodeRef]):
        return State(self.properties, self.node_ref, self.is_reentry, parent_reference, self.header)

    def with_node_ref(self, reference: NodeRef):
        return State(self.properties, reference, self.is_reentry, self.parent_reference, self.header)

    def __setitem__(self, key, value):
        self.properties[key] = value

    def __getitem__(self, item):
        return self.properties[item]
