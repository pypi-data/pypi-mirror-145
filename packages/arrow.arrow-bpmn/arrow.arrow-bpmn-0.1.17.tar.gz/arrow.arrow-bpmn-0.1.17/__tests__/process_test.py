import logging
import unittest
from pathlib import Path

from arrow_bpmn.engine.sequential_bpmn_engine import SequentialBpmnEngine
from arrow_bpmn.parser.json.json_bpmn_parser import JsonBpmnParser
from arrow_bpmn.parser.xml.arrow_xml_bpmn_parser import ArrowXmlBpmnParser


class ProcessSerializationTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.basicConfig(level=logging.INFO)

    def compare(self, source: str):
        engine = SequentialBpmnEngine(parser=ArrowXmlBpmnParser())
        ref = engine.deploy("customGroup", Path(__file__).parent / source)[0]

        parser = JsonBpmnParser()

        process1 = engine.process_store.read_process(ref)
        process2 = parser.parse(process1.to_json())[1][0]

        self.assertEqual(process1.to_json(), process2.to_json())

    def test_script_task(self):
        self.compare("diagrams/script_task.bpmn")

    def test_exclusive_gateway(self):
        self.compare("diagrams/exclusive_gateway.bpmn")

    def test_exclusive_gateway_with_default(self):
        self.compare("diagrams/exclusive_gateway_with_default.bpmn")

    def test_message_start_event(self):
        self.compare("diagrams/message_start_event.bpmn")

    def test_signal_start_event(self):
        self.compare("diagrams/signal_start_event.bpmn")

    def test_call_activity(self):
        self.compare("diagrams/call_activity.bpmn")

    def test_error_boundary_event(self):
        self.compare("diagrams/error_boundary_event.bpmn")

    def test_message_intermediate_throw_event(self):
        self.compare("diagrams/message_intermediate_throw_event.bpmn")

    def test_message_intermediate_catch_event(self):
        self.compare("diagrams/message_intermediate_catch_event.bpmn")

    def test_signal_intermediate_throw_event(self):
        self.compare("diagrams/signal_intermediate_throw_event.bpmn")

    def test_signal_intermediate_catch_event(self):
        self.compare("diagrams/signal_intermediate_catch_event.bpmn")

    def test_user_task(self):
        self.compare("diagrams/user_task.bpmn")

    def test_manual_task(self):
        self.compare("diagrams/manual_task.bpmn")

    def test_send_task(self):
        self.compare("diagrams/send_task.bpmn")

    def test_receive_task(self):
        self.compare("diagrams/receive_task.bpmn")

    def test_service_task(self):
        self.compare("diagrams/service_task.bpmn")

    def test_http_task(self):
        self.compare("diagrams/http_task.bpmn")