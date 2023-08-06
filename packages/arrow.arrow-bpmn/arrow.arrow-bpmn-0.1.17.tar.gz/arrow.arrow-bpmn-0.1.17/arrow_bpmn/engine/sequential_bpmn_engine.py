import logging
import uuid
from typing import List

from arrow_bpmn.__spi__ import CompleteAction, IncidentAction
from arrow_bpmn.__spi__ import NodeRef
from arrow_bpmn.__spi__.action import Action, EventAction
from arrow_bpmn.__spi__.action import ContinueAction
from arrow_bpmn.__spi__.action.cascade_action import CascadeAction
from arrow_bpmn.__spi__.action.dequeue_action import DequeueAction
from arrow_bpmn.__spi__.action.queue_action import QueueAction
from arrow_bpmn.__spi__.action.resume_action import ResumeAction
from arrow_bpmn.__spi__.execution import Environment
from arrow_bpmn.__spi__.execution import State
from arrow_bpmn.__spi__.registry.event import Event
from arrow_bpmn.__spi__.types import OptDict
from arrow_bpmn.engine.abstract_engine import BpmnEngine, ProcessRef
from arrow_bpmn.engine.registry.abstract_event_registry import NoneEvent


def flatten(iterable):
    return [item for sublist in iterable for item in sublist]


def first(iterable):
    return iterable[0]


class SequentialBpmnEngine(BpmnEngine):

    def invoke_by_event(self, event: Event, init_state: OptDict = None, header: OptDict = None) -> List[State]:
        def invoke(node_ref: NodeRef) -> List[State]:
            process = self.process_store.read_process(ProcessRef(event.group, node_ref.process_id))
            environment = Environment(event.group, process, self.factories)

            if environment.is_start_event(node_ref.node_id):
                state = State(init_state or {}, node_ref, header=header or {})
                return self._handle_action(ContinueAction(node_ref.node_id), state, environment)
            return []

        subscriptions = self.event_registry.get_subscriptions(event)
        assert len(subscriptions) > 0, "no subscriptions found"
        return flatten(list(map(invoke, subscriptions))) + self.resume_by_event(event, init_state, header)

    def resume_by_event(self, event: Event, state: dict, header: dict, is_reentry: bool = True) -> List[State]:
        def resume(node_ref: NodeRef) -> List[State]:
            process = self.process_store.read_process(ProcessRef(event.group, node_ref.process_id))
            environment = Environment(event.group, process, self.factories)

            if not environment.is_start_event(node_ref.node_id):
                new_state = self.process_store.read_state(node_ref)
                new_state.properties.update(state or {})
                new_state.header.update(header or {})
                new_state.is_reentry = is_reentry

                action = ContinueAction(node_ref.node_id)
                return self._handle_action(action, new_state, environment)
            else:
                return []

        subscriptions = self.event_registry.get_subscriptions(event)
        return flatten(list(map(resume, subscriptions)))

    def invoke_by_id(self, ref: ProcessRef, init_state: OptDict = None, header: OptDict = None) -> State:
        states = self.invoke_by_event(NoneEvent(ref.group, ref.process_id), init_state, header)
        assert len(states) > 0, "error while invoking process"
        return states[0]

    # noinspection DuplicatedCode
    def _handle_action(self, action: Action, state: State, env: Environment) -> List[State]:
        logging.info(action)
        [listener.on_action(action, state, env) for listener in self.listeners]

        # Continue Action
        # ***************
        if isinstance(action, ContinueAction):
            node = self.interceptor(env.get_node(action.id))
            assert node is not None, f"no node found with id {action.id}"

            node_ref = NodeRef(env.group, state.node_ref.process_id, action.id, str(uuid.uuid4()), str(uuid.uuid4()))
            new_state = state.with_node_ref(node_ref)

            # execute all present boundary events in order to register their events
            [self._handle_action(ContinueAction(e.id), state, env) for e in env.get_boundary_events(node.id)]

            [x.before_node_execution(node, new_state) for x in self.listeners]
            new_state, next_actions = node.execute(new_state, env)
            [x.after_node_execution(node, new_state) for x in self.listeners]

            return flatten([self._handle_action(action, new_state, env) for action in next_actions])

        # Complete Action
        # ***************
        elif isinstance(action, CompleteAction):
            # remove all registered boundary events from the completed node
            for event in env.get_boundary_events(action.id):
                self._handle_action(DequeueAction(event.attached_to_ref), state, env)

            if action.save_state:
                self.process_store.write_state(state)

            if env.is_end_event(action.id):
                if state.parent_reference is not None:
                    return self._handle_action(ResumeAction(state.parent_reference), state, env)

            if action.consume_token:
                return [state]

            return []

        # Queue Action
        # ************
        elif isinstance(action, QueueAction):
            if action.save_state:
                self.process_store.write_state(state)

            if action.event is not None:
                # register an event subscription to get ready for an ResumeAction
                self.event_registry.create_subscription(action.event, state.node_ref, action.consumable)
                # return the state as the intermediate result of the process
                return [state]

            return []

        # Dequeue Action
        # ************
        elif isinstance(action, DequeueAction):
            self.event_registry.delete_subscription(action.event, state.node_ref)

            return []

        # Cascade Action
        # **************
        elif isinstance(action, CascadeAction):
            event = NoneEvent(env.group, action.process_id)
            subscription = first(self.event_registry.get_subscriptions(event))

            process = self.process_store.read_process(ProcessRef(event.group, subscription.process_id))
            new_state = State(action.init_state, subscription, False, action.parent_reference, state.header)
            new_environment = Environment(event.group, process, self.factories)

            new_state = first(self._handle_action(ContinueAction(subscription.node_id), new_state, new_environment))
            return [new_state]

        # Resume Action
        # *************
        elif isinstance(action, ResumeAction):
            parent_process = self.process_store.read_process(ProcessRef(env.group, action.reference.process_id))
            next_env = Environment(env.group, parent_process, self.factories)
            next_state = State(state.properties, action.reference, True, None, state.header)

            node = next_env.get_node(action.reference.node_id)
            assert node is not None, f"no node found with id {action.reference.node_id}"

            [x.before_node_execution(node, state) for x in self.listeners]
            new_state, next_actions = node.execute(next_state, next_env)
            [x.after_node_execution(node, state) for x in self.listeners]

            return flatten([self._handle_action(action, new_state, next_env) for action in next_actions])

        # Incident Action
        # ***************
        elif isinstance(action, IncidentAction):
            self.incident_handler.handle(action)
            return []

        # Event Action
        # ************
        elif isinstance(action, EventAction):
            next_actions = self.event_emitter.emit(action.event, self.event_registry)
            return flatten([self._handle_action(action, state, env) for action in next_actions])

        else:
            raise ValueError("cannot handle action " + str(action))
