import logging
import unittest
from pathlib import Path

from arrow_bpmn.engine.sequential_bpmn_engine import SequentialBpmnEngine
from arrow_bpmn.parser.xml.arrow_xml_bpmn_parser import ArrowXmlBpmnParser


class ExtensionTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.basicConfig(level=logging.INFO)

    def test_initiate_expression(self):
        engine = SequentialBpmnEngine(parser=ArrowXmlBpmnParser())
        ref = engine.deploy("customGroup", Path(__file__).parent / "diagrams/extension/initiate_expression.bpmn")[0]

        state = engine.invoke_by_id(ref, {"A": False})
        self.assertEqual(state.properties, {"A": True, "B": True})

    def test_continue_expression(self):
        engine = SequentialBpmnEngine(parser=ArrowXmlBpmnParser())
        ref = engine.deploy("customGroup", Path(__file__).parent / "diagrams/extension/continue_expression.bpmn")[0]

        state = engine.invoke_by_id(ref, {"A": False})
        self.assertEqual(state.properties, {"A": False, "B": True})

    def test_complete_expression(self):
        engine = SequentialBpmnEngine(parser=ArrowXmlBpmnParser())
        ref = engine.deploy("customGroup", Path(__file__).parent / "diagrams/extension/complete_expression.bpmn")[0]

        state = engine.invoke_by_id(ref, {"A": False})
        self.assertEqual(state.properties, {"A": False, "B": True, "C": True})
