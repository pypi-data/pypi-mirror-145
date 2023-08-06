import xml.etree.ElementTree as XmlTree
from typing import List, Optional

NAMESPACES = {
    "bpmn": "http://www.omg.org/spec/BPMN/20100524/MODEL",
    "arrow": "http://www.x-and-y.ai/schema/bpmn/arrow"
}


class XMLElement:

    def __init__(self, element: XmlTree.Element):
        self.element = element

    def get_tags(self, tag: str, namespaces: Optional[dict] = None) -> List['XMLElement']:
        elements = self.element.findall(tag, namespaces or NAMESPACES)
        return list(map(lambda x: XMLElement(x), elements))

    def has_tag(self, tag: str, namespaces: Optional[dict] = None) -> bool:
        return self.get_tag(tag, namespaces) is not None

    def get_tag(self, tag: str, namespaces: Optional[dict] = None) -> Optional['XMLElement']:
        elements = self.element.findall(tag, namespaces or NAMESPACES)
        if len(elements) == 0:
            return None
        return next(map(lambda x: XMLElement(x), elements))

    def has_attribute(self, name: str, namespaces: Optional[dict] = None):
        return self.get_attribute(name, namespaces) is not None

    def get_attributes(self):
        return {x[0]: x[1] for x in self.element.items()}

    def get_attribute(self, name: str, namespaces: Optional[dict] = None, default_value=None) -> Optional[str]:
        attributes = self.get_attributes()

        if ":" in name:
            array = name.split(":")
            namespace = (namespaces or NAMESPACES)[array[0]]
            key = "{" + namespace + "}" + array[1]
            return attributes[key] if key in attributes else default_value

        return attributes[name] if name in attributes else default_value

    def get_text(self, unescape: bool = False) -> Optional[str]:
        if self.element.text is None:
            return None

        if unescape:
            import xml.sax.saxutils as sax
            return sax.unescape(self.element.text.strip())
        return self.element.text.strip()

    def __getitem__(self, item):
        return self.get_attribute(item)
