import logging
from typing import OrderedDict, Optional, TypeVar, Generic

from arrow_bpmn.__spi__ import State, NodeRef
from arrow_bpmn.engine.registry.abstract_event_registry import ProcessRef
from arrow_bpmn.engine.store.abstract_process_store import ProcessStore
from arrow_bpmn.model.process import Process

T = TypeVar("T")


class LRUCache(OrderedDict, Generic[T]):

    def __init__(self, cache_size: int):
        super().__init__()
        self.cache_size = cache_size

    def __getitem__(self, item: str) -> Optional[T]:
        if item in self:
            logging.info(f"cache hit for {item}")
            self.move_to_end(item, last=True)
            return super().__getitem__(item)
        return None

    def __setitem__(self, key: str, value: T):
        super().__setitem__(key, value)
        if len(self) > self.cache_size:
            evict_key, evict_val = self.popitem(last=False)
            logging.info(f"evict item from LRU cache {evict_key}={evict_val}")


class CacheableProcessStoreAdapter(ProcessStore):

    def __init__(self, process_store: ProcessStore, cache_size: int = 128):
        self.delegate = process_store
        self.process_cache = LRUCache[Process](cache_size)
        self.state_cache = LRUCache[State](cache_size)

    def write_process(self, group: str, process: Process):
        self.process_cache[group + ":" + process.id] = process
        self.delegate.write_process(group, process)

    def read_process(self, ref: ProcessRef) -> Optional[Process]:
        if str(ref) in self.process_cache:
            return self.process_cache[str(ref)]
        return self.delegate.read_process(ref)

    def write_state(self, state: State):
        self.state_cache[str(state.node_ref)] = state
        self.delegate.write_state(state)

    def read_state(self, ref: NodeRef) -> State:
        if str(ref) in self.state_cache:
            return self.state_cache[str(ref)]
        return self.delegate.read_state(ref)
