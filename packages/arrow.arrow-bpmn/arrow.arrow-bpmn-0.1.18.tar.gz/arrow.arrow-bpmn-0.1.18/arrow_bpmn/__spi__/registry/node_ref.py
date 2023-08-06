from dataclasses import dataclass
from typing import Optional

from arrow_bpmn.__spi__.registry.process_ref import ProcessRef


@dataclass
class NodeRef(ProcessRef):
    """
    The NodeRef class is used to define the node invocation target of an event.
    This implementation can point to a start event, task or intermediate catching event.

    While a start event only has a process id and a node id a task and intermediate catching event
    needs the process instance id and node instance id as well.
    """

    node_id: str
    process_instance_id: Optional[str] = None
    node_instance_id: Optional[str] = None

    @staticmethod
    def parse(text: str):
        array = text.split(":")
        assert len(array) == 3 or len(array) == 5, "invalid node ref string representation"

        if len(array) == 3:
            return NodeRef(array[0], array[1], array[2])
        return NodeRef(array[0], array[1], array[2], array[3], array[4])

    def __repr__(self):
        if self.process_instance_id is not None and self.node_instance_id is not None:
            return self.group + ":" + self.process_id + ":" + self.node_id + ":" + self.process_instance_id + ":" + self.node_instance_id
        return self.group + ":" + self.process_id + ":" + self.node_id

    def __iter__(self):
        return iter((self.group, self.process_id, self.node_id, self.process_instance_id, self.node_instance_id))
