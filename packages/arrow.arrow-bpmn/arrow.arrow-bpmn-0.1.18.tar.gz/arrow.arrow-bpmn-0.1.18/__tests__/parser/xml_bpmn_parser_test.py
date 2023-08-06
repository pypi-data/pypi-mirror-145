import logging
import unittest
from pathlib import Path

from arrow_bpmn.parser.xml.xml_bpmn_parser import XmlBpmnParser


class XmlBpmnParserTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.basicConfig(level=logging.INFO)

    def test_parse_string(self):
        with open(Path(__file__).parent.parent / "diagrams/extension/initiate_expression.bpmn", "r") as file:
            bpmn_xml = file.read()
            process = XmlBpmnParser().parse(bpmn_xml)[0]
            self.assertTrue(process is not None)

    def test_parse_string2(self):
        with open(Path(__file__).parent / "test.xml", "r") as file:
            bpmn_xml = file.read()
            process = XmlBpmnParser().parse(bpmn_xml)[0]
            self.assertTrue(process is not None)