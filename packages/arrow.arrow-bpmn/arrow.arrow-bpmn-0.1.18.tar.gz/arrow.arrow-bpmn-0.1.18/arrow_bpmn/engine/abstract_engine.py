import logging
from dataclasses import dataclass, field
from typing import List

from arrow_dmn.engine.sync_dmn_engine import SyncDmnEngine

from arrow_bpmn.__spi__.execution import State
from arrow_bpmn.__spi__.execution.event_emitter import EventEmitter
from arrow_bpmn.__spi__.execution.incident_handler import IncidentHandler, LoggingIncidentHandler
from arrow_bpmn.__spi__.factory import BpmnFactories, ServiceFactory
from arrow_bpmn.__spi__.factory.business_rule_factory import BusinessRuleFactory
from arrow_bpmn.__spi__.factory.script_factory import ScriptFactory
from arrow_bpmn.__spi__.factory.service_factory import NoOpServiceFactory
from arrow_bpmn.__spi__.registry.event import Event
from arrow_bpmn.__spi__.types import BpmnSource, OptDict
from arrow_bpmn.engine.event.eager_event_emitter import EagerEventEmitter
from arrow_bpmn.engine.execution.cacheable_script_factory import CacheableScriptFactory
from arrow_bpmn.engine.interceptor.abstract_bpmn_engine_interceptor import BpmnEngineInterceptor
from arrow_bpmn.engine.interceptor.arrow_extension_interceptor import ArrowExtensionInterceptor
from arrow_bpmn.engine.listener.abstract_bpmn_engine_listener import BpmnEngineListener
from arrow_bpmn.engine.registry.abstract_event_registry import EventRegistry, ProcessRef
from arrow_bpmn.engine.registry.inmemory_event_registry import InMemoryEventRegistry
from arrow_bpmn.engine.store.abstract_process_store import ProcessStore
from arrow_bpmn.engine.store.inmemory_process_store import InMemoryProcessStore
from arrow_bpmn.parser.abstract_parser import BpmnParser
from arrow_bpmn.parser.xml.xml_bpmn_parser import XmlBpmnParser


@dataclass
class BpmnEngine:
    parser: BpmnParser = field(default_factory=lambda: XmlBpmnParser())
    event_registry: EventRegistry = field(default_factory=lambda: InMemoryEventRegistry())
    process_store: ProcessStore = field(default_factory=lambda: InMemoryProcessStore())
    listeners: List[BpmnEngineListener] = field(default_factory=lambda: [])
    incident_handler: IncidentHandler = field(default_factory=lambda: LoggingIncidentHandler())
    event_emitter: EventEmitter = field(default_factory=lambda: EagerEventEmitter())
    script_factory: ScriptFactory = field(default_factory=lambda: CacheableScriptFactory(128))
    service_factory: ServiceFactory = field(default_factory=lambda: NoOpServiceFactory())
    business_rule_factory: BusinessRuleFactory = field(default_factory=lambda: SyncDmnEngine())
    interceptor: BpmnEngineInterceptor = field(default_factory=lambda: ArrowExtensionInterceptor())

    def __post_init__(self):
        self.factories = BpmnFactories(self.script_factory, self.service_factory, self.business_rule_factory)

    def deploy(self, group: str, source: BpmnSource) -> List[ProcessRef]:
        deployed_processes = []
        processes = self.parser.parse(source)
        for process in processes:
            process_ref = ProcessRef(group, process.id)
            if self.process_store.has_process(process_ref):
                logging.info("process already deployed, start undeploying process")
                self.undeploy(process_ref)

            process.with_event_registry(process_ref, self.event_registry)
            self.process_store.write_process(group, process)

            deployed_processes.append(process_ref)

        return deployed_processes

    def undeploy(self, process_ref: ProcessRef):
        self.event_registry.delete_subscriptions(process_ref)
        self.process_store.delete_process(process_ref)

    def invoke_by_event(self, event: Event, init_state: OptDict = None) -> List[State]:
        pass

    def resume_by_event(self, event: Event, state: dict, header: dict, is_reentry: bool = True) -> List[State]:
        pass

    def invoke_by_id(self, process: ProcessRef, init_state: OptDict = None) -> State:
        pass
