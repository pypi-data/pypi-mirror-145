from typing import List


class Environment:

    def __init__(self, group: str, process, factories):
        self.group = group
        self.process_id = process.id
        self.nodes = {}
        self.event_specs = process.events
        for task in process.tasks:
            self.nodes[task.id] = task
        for event in process.start_events:
            self.nodes[event.id] = event
        for event in process.end_events:
            self.nodes[event.id] = event
        for event in process.boundary_events:
            self.nodes[event.id] = event
        for node in process.intermediate_events:
            self.nodes[node.id] = node
        for gateway in process.gateways:
            self.nodes[gateway.id] = gateway

        self.edges = {}
        for flow in process.sequence_flows:
            self.edges[flow.id] = flow

        self.outgoing_edges = {}
        for flow in process.sequence_flows:
            if flow.source_ref not in self.outgoing_edges:
                self.outgoing_edges[flow.source_ref] = []

            self.outgoing_edges[flow.source_ref].append(flow)

        self.attached_nodes = {}
        for event in process.boundary_events:
            if event.attached_to_ref not in self.attached_nodes:
                self.attached_nodes[event.attached_to_ref] = []

            self.attached_nodes[event.attached_to_ref].append(event)

        self.script_factory = factories.script_factory
        self.service_factory = factories.service_factory
        self.business_rule_factory = factories.business_rule_factory

    def get_node(self, node_id: str):
        return self.nodes[node_id] if node_id in self.nodes else None

    def get_edge(self, edge_id):
        return self.edges[edge_id] if edge_id in self.edges else None

    def get_incoming_edges(self, node_id: str):
        raise ValueError("not implemented")

    def get_outgoing_edges(self, node_id: str):
        return self.outgoing_edges[node_id]

    def get_outgoing_nodes(self, node_id: str):
        return list(map(lambda x: x.target_ref, self.outgoing_edges[node_id]))

    def get_boundary_events(self, node_id: str) -> List:
        return self.attached_nodes[node_id] if node_id in self.attached_nodes else []

    def is_start_event(self, node_id: str) -> bool:
        if node_id in self.nodes:
            return "StartEvent" in type(self.nodes[node_id]).__name__
        return False

    def is_end_event(self, node_id: str) -> bool:
        if node_id in self.nodes:
            return "EndEvent" in type(self.nodes[node_id]).__name__
        return False

    def get_message(self, message_ref: str):
        return self.event_specs.messages[message_ref]
