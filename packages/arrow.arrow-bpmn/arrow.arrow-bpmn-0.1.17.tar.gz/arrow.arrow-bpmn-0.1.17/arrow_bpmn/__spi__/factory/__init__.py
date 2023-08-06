from dataclasses import dataclass

from arrow_bpmn.__spi__.factory.business_rule_factory import BusinessRuleFactory
from arrow_bpmn.__spi__.factory.script_factory import ScriptFactory
from arrow_bpmn.__spi__.factory.service_factory import ServiceFactory


@dataclass
class BpmnFactories:
    script_factory: ScriptFactory
    service_factory: ServiceFactory
    business_rule_factory: BusinessRuleFactory
