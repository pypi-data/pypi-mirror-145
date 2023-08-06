import json
from typing import Tuple, List

from arrow_bpmn.__spi__.types import BpmnSource
from arrow_bpmn.model.event.boundary.error_boundary_event import ErrorBoundaryEvent
from arrow_bpmn.model.event.endevent.error_end_event import ErrorEndEvent
from arrow_bpmn.model.event.endevent.message_end_event import MessageEndEvent
from arrow_bpmn.model.event.endevent.none_end_event import NoneEndEvent
from arrow_bpmn.model.event.endevent.signal_end_event import SignalEndEvent
from arrow_bpmn.model.event.intermediate.message_intermediate_catch_event import MessageIntermediateCatchEvent
from arrow_bpmn.model.event.intermediate.message_intermediate_throw_event import MessageIntermediateThrowEvent
from arrow_bpmn.model.event.intermediate.signal_intermediate_catch_event import SignalIntermediateCatchEvent
from arrow_bpmn.model.event.intermediate.signal_intermediate_throw_event import SignalIntermediateThrowEvent
from arrow_bpmn.model.event.startevent.message_start_event import MessageStartEvent
from arrow_bpmn.model.event.startevent.none_start_event import NoneStartEvent
from arrow_bpmn.model.event.startevent.signal_start_event import SignalStartEvent
from arrow_bpmn.model.gateway.exclusive_gateway import ExclusiveGateway
from arrow_bpmn.model.process import Process, EventDict
from arrow_bpmn.model.sequence.association import Association
from arrow_bpmn.model.sequence.sequence_flow import SequenceFlow
from arrow_bpmn.model.task.business_rule_task import BusinessRuleTask
from arrow_bpmn.model.task.call_activity import CallActivity, VariableMapping, ExpressionMapping
from arrow_bpmn.model.task.extension.http_task import HttpTask
from arrow_bpmn.model.task.manual_task import ManualTask
from arrow_bpmn.model.task.receive_task import ReceiveTask
from arrow_bpmn.model.task.script_task import ScriptTask
from arrow_bpmn.model.task.send_task import SendTask
from arrow_bpmn.model.task.service_task import ServiceTask
from arrow_bpmn.model.task.user_task import UserTask
from arrow_bpmn.parser.abstract_parser import BpmnParser
from arrow_bpmn.parser.json.json_element import JSONElement


def unwrap(attributes: dict):
    for k in attributes:
        value = attributes[k]
        if isinstance(value, dict) and "type" in value and "item" in value:
            attributes[k] = value["item"]
    return attributes


class JsonBpmnParser(BpmnParser):

    def parse(self, source: BpmnSource) -> Tuple[str, List[Process]]:
        element = JSONElement(json.loads(source))
        # group = element["group"]

        sequence_flows = [self._parse_sequence_flow(JSONElement(x)) for x in element.pop("sequence_flows")]
        associations = [self._parse_association(JSONElement(x)) for x in element.pop("associations")]
        start_events = [self._parse_start_event(JSONElement(x)) for x in element.pop("start_events")]
        end_events = [self._parse_end_event(JSONElement(x)) for x in element.pop("end_events")]
        boundary_events = [self._parse_boundary_event(JSONElement(x)) for x in element.pop("boundary_events")]
        intermediate_events = [self._parse_intermediate_event(JSONElement(x)) for x in
                               element.pop("intermediate_events")]
        tasks = [self._parse_task(JSONElement(x)) for x in element.pop("tasks")]
        gateways = [self._parse_gateway(JSONElement(x)) for x in element.pop("gateways")]

        events = element.pop("events")
        events = EventDict(events["item"])

        return "group", [Process(element.as_dict(), sequence_flows, associations, tasks, start_events, end_events,
                                 boundary_events, intermediate_events, gateways, events)]

    def _parse_sequence_flow(self, element: JSONElement):
        return SequenceFlow.from_json(element.get_object("item"))

    def _parse_association(self, element: JSONElement):
        return Association(element.get_object("item").as_dict())

    def _parse_start_event(self, element: JSONElement):
        _type = element["type"]
        _item = element.get_object("item")

        if _type == "NoneStartEvent":
            return NoneStartEvent(_item.as_dict())
        if _type == "MessageStartEvent":
            message = _item.pop("message")
            return MessageStartEvent(_item.as_dict(), message)
        if _type == "SignalStartEvent":
            signal = _item.pop("signal")
            return SignalStartEvent(_item.as_dict(), signal)

        raise ValueError(f"cannot parse element with type {element['type']}")

    def _parse_end_event(self, element: JSONElement):
        _type = element["type"]
        _item = element.get_object("item")

        if _type == "NoneEndEvent":
            return NoneEndEvent(_item.as_dict())
        if _type == "MessageEndEvent":
            message = element.pop("message")
            return MessageEndEvent(_item.as_dict(), message)
        if _type == "SignalEndEvent":
            signal = element.pop("signal")
            return SignalEndEvent(_item.as_dict(), signal)
        if _type == "ErrorEndEvent":
            error = element.pop("error")
            return ErrorEndEvent(_item.as_dict(), error)

        raise ValueError(f"cannot parse element with type {element['type']}")

    def _parse_boundary_event(self, element: JSONElement):
        _type = element["type"]
        _item = element.get_object("item")

        if _type == "ErrorBoundaryEvent":
            error = _item.pop("error")
            return ErrorBoundaryEvent(_item.as_dict(), error)

        raise ValueError(f"cannot parse element with type {element['type']}")

    def _parse_intermediate_event(self, element: JSONElement):
        _type = element["type"]
        _item = element.get_object("item")

        if _type == "MessageIntermediateCatchEvent":
            message = _item.pop("message")
            return MessageIntermediateCatchEvent(_item.as_dict(), message)
        if _type == "MessageIntermediateThrowEvent":
            message = _item.pop("message")
            return MessageIntermediateThrowEvent(_item.as_dict(), message)
        if _type == "SignalIntermediateCatchEvent":
            signal = _item.pop("signal")
            return SignalIntermediateCatchEvent(_item.as_dict(), signal)
        if _type == "SignalIntermediateThrowEvent":
            signal = _item.pop("signal")
            return SignalIntermediateThrowEvent(_item.as_dict(), signal)

        raise ValueError(f"cannot parse element with type {element['type']}")

    def _parse_task(self, element: JSONElement):
        _type = element["type"]
        _item = element.get_object("item")

        attributes = _item.as_dict()

        if _type == "BusinessRuleTask":
            return BusinessRuleTask(attributes)
        if _type == "CallActivity":
            incoming_state = list(map(lambda x: JSONElement(x), _item.pop("incoming_state")))
            incoming_state = list(map(self._parse_state_mapping, incoming_state))
            outgoing_state = list(map(lambda x: JSONElement(x), _item.pop("outgoing_state")))
            outgoing_state = list(map(self._parse_state_mapping, outgoing_state))

            return CallActivity(attributes, incoming_state, outgoing_state)
        if _type == "ManualTask":
            return ManualTask(attributes)
        if _type == "UserTask":
            return UserTask(attributes)
        if _type == "ReceiveTask":
            return ReceiveTask(attributes)
        if _type == "ScriptTask":
            return ScriptTask(attributes)
        if _type == "SendTask":
            return SendTask(attributes)
        if _type == "ServiceTask":
            return ServiceTask(attributes)

        # TODO: move to ArrowJsonBpmnParser
        if _type == "HttpTask":
            return HttpTask(unwrap(attributes))

        raise ValueError(f"cannot parse element with type {element['type']}")

    def _parse_gateway(self, element: JSONElement):
        _type = element["type"]
        _item = element.get_object("item")

        if _type == "ExclusiveGateway":
            return ExclusiveGateway(_item.as_dict())

        raise ValueError(f"cannot parse element with type {element['type']}")

    def _parse_state_mapping(self, element: JSONElement):
        _type = element["type"]
        _item = element.get_object("item")

        if _type == "VariableMapping":
            return VariableMapping(_item["source"], _item["target"])
        if _type == "ExpressionMapping":
            return ExpressionMapping(_item["source"], _item["target"])

        raise ValueError(f"cannot parse element with type {element['type']}")
