import logging
import unittest
from pathlib import Path
from typing import Tuple

from arrow_bpmn.__spi__ import State, Environment, CompleteAction
from arrow_bpmn.__spi__.action import Actions, ContinueAction
from arrow_bpmn.__spi__.execution.executable import Executable
from arrow_bpmn.__spi__.factory.service_factory import LambdaServiceFactory
from arrow_bpmn.engine.event.bucket_event_emitter import BucketEventEmitter
from arrow_bpmn.engine.registry.abstract_event_registry import MessageEvent, SignalEvent, UserEvent, \
    ManualEvent
from arrow_bpmn.engine.sequential_bpmn_engine import SequentialBpmnEngine
from arrow_bpmn.parser.xml.arrow_xml_bpmn_parser import ArrowXmlBpmnParser
from arrow_bpmn.parser.xml.xml_bpmn_parser import XmlBpmnParser


class SequentialBpmnEngineTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.basicConfig(level=logging.INFO)

    def test_script_task(self):
        engine = SequentialBpmnEngine()
        ref = engine.deploy("customGroup", Path(__file__).parent / "diagrams/script_task.bpmn")[0]

        state = engine.invoke_by_id(ref, {"n": 8})
        self.assertEqual(state["test"], 21)

    def test_exclusive_gateway(self):
        engine = SequentialBpmnEngine()
        ref = engine.deploy("customGroup", Path(__file__).parent / "diagrams/exclusive_gateway.bpmn")[0]

        state = engine.invoke_by_id(ref, {"flag": True})
        self.assertEqual(state["result"], 10)

    def test_exclusive_gateway_with_default(self):
        engine = SequentialBpmnEngine()
        ref = engine.deploy("customGroup", Path(__file__).parent / "diagrams/exclusive_gateway_with_default.bpmn")[0]

        state = engine.invoke_by_id(ref, {"flag": False})
        self.assertEqual(state["result"], 20)

    def test_message_start_event(self):
        engine = SequentialBpmnEngine()
        _ = engine.deploy("customGroup", Path(__file__).parent / "diagrams/message_start_event.bpmn")[0]

        state = engine.invoke_by_event(MessageEvent("customGroup", "custom-message"))[0]
        self.assertEqual(state["test"], True)

    def test_signal_start_event(self):
        engine = SequentialBpmnEngine()
        _ = engine.deploy("customGroup", Path(__file__).parent / "diagrams/signal_start_event.bpmn")[0]

        state = engine.invoke_by_event(SignalEvent("customGroup", "custom-signal"))[0]
        self.assertEqual(state["test"], True)

    def test_call_activity(self):
        engine = SequentialBpmnEngine()
        ref = engine.deploy("customGroup", Path(__file__).parent / "diagrams/call_activity.bpmn")[0]

        engine.invoke_by_id(ref, {"x": 5}, {"id": 123})
        state = engine.invoke_by_event(ManualEvent("customGroup", "subprocess", "task2", {}))[0]
        self.assertAlmostEqual(state["y1"], 7.5)
        self.assertAlmostEqual(state["y2"], 15)

    def test_error_boundary_event(self):
        engine = SequentialBpmnEngine()
        ref = engine.deploy("customGroup", Path(__file__).parent / "diagrams/error_boundary_event.bpmn")[0]

        engine.invoke_by_id(ref, {"x": 5})

    # noinspection PyUnresolvedReferences
    def test_message_intermediate_throw_event(self):
        engine = SequentialBpmnEngine(event_emitter=BucketEventEmitter())
        ref = engine.deploy("customGroup", Path(__file__).parent / "diagrams/message_intermediate_throw_event.bpmn")[0]

        engine.invoke_by_id(ref, {"x": 5})
        self.assertEqual(len(engine.event_emitter.bucket), 1)
        self.assertEqual(engine.event_emitter.bucket[0].name, "custom-message")

    def test_message_intermediate_catch_event(self):
        engine = SequentialBpmnEngine(event_emitter=BucketEventEmitter())
        ref = engine.deploy("customGroup", Path(__file__).parent / "diagrams/message_intermediate_catch_event.bpmn")[0]

        engine.invoke_by_id(ref)
        engine.invoke_by_event(MessageEvent("customGroup", "custom-message"))

    # noinspection PyUnresolvedReferences
    def test_signal_intermediate_throw_event(self):
        engine = SequentialBpmnEngine(event_emitter=BucketEventEmitter())
        ref = engine.deploy("customGroup", Path(__file__).parent / "diagrams/signal_intermediate_throw_event.bpmn")[0]

        engine.invoke_by_id(ref, {"x": 5})
        self.assertEqual(len(engine.event_emitter.bucket), 1)
        self.assertEqual(engine.event_emitter.bucket[0].name, "custom-signal")

    def test_signal_intermediate_catch_event(self):
        engine = SequentialBpmnEngine(event_emitter=BucketEventEmitter())
        ref = engine.deploy("customGroup", Path(__file__).parent / "diagrams/signal_intermediate_catch_event.bpmn")[0]

        engine.invoke_by_id(ref)
        engine.invoke_by_event(SignalEvent("customGroup", "custom-signal"))

    def test_user_task(self):
        engine = SequentialBpmnEngine(event_emitter=BucketEventEmitter())
        ref = engine.deploy("customGroup", Path(__file__).parent / "diagrams/user_task.bpmn")[0]

        engine.invoke_by_id(ref)
        engine.invoke_by_event(UserEvent("customGroup", "Process_0elkd69", "task", {}))

    def test_manual_task(self):
        engine = SequentialBpmnEngine(event_emitter=BucketEventEmitter())
        ref = engine.deploy("customGroup", Path(__file__).parent / "diagrams/manual_task.bpmn")[0]

        engine.invoke_by_id(ref)
        engine.invoke_by_event(ManualEvent("customGroup", "Process_0elkd69", "task", {}))

    # noinspection PyUnresolvedReferences
    def test_send_task(self):
        engine = SequentialBpmnEngine(event_emitter=BucketEventEmitter())
        ref = engine.deploy("customGroup", Path(__file__).parent / "diagrams/send_task.bpmn")[0]

        engine.invoke_by_id(ref, {"x": 5})
        self.assertEqual(len(engine.event_emitter.bucket), 1)
        self.assertEqual(engine.event_emitter.bucket[0].name, "custom-message")

    def test_receive_task(self):
        engine = SequentialBpmnEngine(event_emitter=BucketEventEmitter())
        ref = engine.deploy("customGroup", Path(__file__).parent / "diagrams/receive_task.bpmn")[0]

        engine.invoke_by_id(ref)
        engine.invoke_by_event(MessageEvent("customGroup", "custom-message"))

    def test_service_task(self):
        class ServiceDelegate(Executable):

            def execute(self, state: State, environment: Environment) -> Tuple[State, Actions]:
                state["custom"] = "test"
                actions = [ContinueAction(node) for node in environment.get_outgoing_nodes(state.node_ref.node_id)]
                return state, [CompleteAction(state.node_ref.node_id)] + actions

        service_factory = LambdaServiceFactory(lambda x, y: ServiceDelegate())
        engine = SequentialBpmnEngine(parser=XmlBpmnParser(), service_factory=service_factory)
        ref = engine.deploy("customGroup", Path(__file__).parent / "diagrams/service_task.bpmn")[0]

        state = engine.invoke_by_id(ref)
        self.assertEqual(state["custom"], "test")

    def test_http_task(self):
        engine = SequentialBpmnEngine(parser=ArrowXmlBpmnParser())
        ref = engine.deploy("customGroup", Path(__file__).parent / "diagrams/http_task.bpmn")[0]

        state = engine.invoke_by_id(ref)
        self.assertEqual(state["result"], "Luke Skywalker")
