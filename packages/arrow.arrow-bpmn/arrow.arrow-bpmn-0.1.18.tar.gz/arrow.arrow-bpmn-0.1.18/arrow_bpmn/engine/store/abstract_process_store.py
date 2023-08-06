from typing import Optional

from arrow_bpmn.__spi__ import State, NodeRef
from arrow_bpmn.__spi__.registry.process_ref import ProcessRef
from arrow_bpmn.model.process import Process


class ProcessStore:

    def write_process(self, group: str, process: Process):
        pass

    def delete_process(self, process_ref: ProcessRef):
        pass

    def read_process(self, ref: ProcessRef) -> Optional[Process]:
        pass

    def has_process(self, ref: ProcessRef) -> bool:
        return self.read_process(ref) is not None

    def write_state(self, state: State):
        pass

    def read_state(self, ref: NodeRef) -> State:
        pass
