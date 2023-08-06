from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, List, Union

from arrow_bpmn.__spi__.registry.event import Event
from arrow_bpmn.__spi__.registry.node_ref import NodeRef
from arrow_bpmn.__spi__.registry.process_ref import ProcessRef

EventStr = str


class EventRegistry(ABC):

    @abstractmethod
    def create_subscription(self, event: Event, node_ref: NodeRef, consumable: bool):
        pass

    @abstractmethod
    def delete_subscription(self, event: Optional[Union[Event, EventStr]], node_ref: NodeRef):
        pass

    @abstractmethod
    def delete_subscriptions(self, process_ref: ProcessRef):
        pass

    @abstractmethod
    def get_subscriptions(self, event: Union[Event, EventStr]) -> List[NodeRef]:
        pass


class EventRegistryAware(ABC):

    def with_event_registry(self, process_ref: ProcessRef, event_registry: EventRegistry):
        pass


@dataclass
class NoneEvent(Event):
    process_id: str

    def __repr__(self):
        return f"NoneEvent({self.group}:{self.process_id})"


@dataclass
class MessageEvent(Event):
    name: str

    def __repr__(self):
        return f"MessageEvent({self.group}:{self.name})"


@dataclass
class TimerEvent(Event):
    pass


@dataclass
class TimerDateEvent(TimerEvent):
    timer_date: str


@dataclass
class TimerCycleEvent(TimerEvent):
    timer_cycle: str


@dataclass
class TimerDurationEvent(TimerEvent):
    timer_duration: str


@dataclass
class SignalEvent(Event):
    name: str

    def __repr__(self):
        return f"SignalEvent({self.group}:{self.name})"


@dataclass
class ErrorEvent(Event):
    error_ref: str


@dataclass
class UserEvent(Event):
    process_id: str
    node_id: str
    attributes: dict

    def __repr__(self):
        return f"UserEvent({self.group}:{self.process_id}:{self.node_id})"


@dataclass
class ManualEvent(Event):
    process_id: str
    node_id: str
    attributes: dict

    def __repr__(self):
        return f"ManualEvent({self.group}:{self.process_id}:{self.node_id})"


@dataclass
class ConditionalEvent(Event):
    condition: str
    context: Optional[dict]

    def __repr__(self):
        return f"ConditionalEvent({self.group}:{self.condition})"


@dataclass
class CompensationEvent(Event):
    process_id: str
    process_instance_id: str

    def __repr__(self):
        return f"CompensationEvent({self.group}:{self.process_id}:{self.process_instance_id})"
