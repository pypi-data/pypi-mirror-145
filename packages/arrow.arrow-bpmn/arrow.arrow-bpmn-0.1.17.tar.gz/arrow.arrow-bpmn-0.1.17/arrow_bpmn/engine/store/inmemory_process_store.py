from typing import Dict, Optional

from arrow_bpmn.__spi__ import State, NodeRef
from arrow_bpmn.engine.registry.abstract_event_registry import ProcessRef
from arrow_bpmn.engine.store.abstract_process_store import ProcessStore
from arrow_bpmn.model.process import Process


class InMemoryProcessStore(ProcessStore):

    def __init__(self):
        self.process_cache: Dict[str, Process] = {}
        self.state_cache: Dict[str, State] = {}

    def write_process(self, group: str, process: Process):
        self.process_cache[group + ":" + process.id] = process

    def delete_process(self, process_ref: ProcessRef):
        del self.process_cache[str(process_ref)]

    def read_process(self, ref: ProcessRef) -> Optional[Process]:
        return self.process_cache[str(ref)] if str(ref) in self.process_cache else None

    def write_state(self, state: State):
        self.state_cache[str(state.node_ref)] = state

    def read_state(self, ref: NodeRef) -> State:
        return self.state_cache[str(ref)]
