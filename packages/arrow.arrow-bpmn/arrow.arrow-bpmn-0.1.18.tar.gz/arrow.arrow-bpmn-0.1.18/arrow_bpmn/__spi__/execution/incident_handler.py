from abc import ABC, abstractmethod

from arrow_bpmn.__spi__ import IncidentAction


class IncidentHandler(ABC):

    @abstractmethod
    def handle(self, action: IncidentAction):
        pass


class LoggingIncidentHandler(IncidentHandler):

    def handle(self, action: IncidentAction):
        import logging
        logging.error(action.error_ref)
        if action.error_msg is not None:
            logging.error(action.error_msg)
