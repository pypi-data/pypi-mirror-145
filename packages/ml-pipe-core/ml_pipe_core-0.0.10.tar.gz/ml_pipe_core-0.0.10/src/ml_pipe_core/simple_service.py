import json
from abc import abstractmethod
from typing import Optional
import requests
import time

from confluent_kafka import TIMESTAMP_NOT_AVAILABLE

from .logger import init_logger
from .config import KAFKA_SERVER_URL, OBSERVER_URL
from .machine_topics import MACHINE_INPUT_TOPIC
from .service import Service
from src.ml_pipe_core.event_utls.consumer import consume
from .message import Headers
from .simple_service_message import SimpleServiceMessage
from .topics import AGENT_EVENTS, RECONFIG_TOPIC, SERVICE_INPUT_TOPIC
from .machine_topics import MACHINE_EVENTS
from .simulation.update_message_types import *
from .agent_result_message import AgentResultMessage
from .adapter.MsgBusWriter import MessageBusWriter
from .simulation.MachineService import MachineService

_logger = init_logger(__name__)


class SimpleService(Service):
    def __init__(self, name, read, write=None, simulations=[]):
        super().__init__(name)
        self.write_hook = MessageBusWriter() if write is None else write
        self.read_hook = read
        self.current_package_id = None
        self.simulations = simulations

    @abstractmethod
    def proposal(self, params: Optional[dict]):
        """[summary]
        Function that will be called when the Agent is triggered.
        :param params: Optional parameter for configuration or setting internal parameter
        :type params: Optional[dict]
        :return: A tuple consisting of a dictionary which is containing the result of the Agent that will be stored,
        an error code and and error message. All parameter are optional and can be set to None if not needed.
        :rtype: Optional[Tuple[dict, int, str]]
        """
        pass

    def async_write(self, channel, device, _property, **kwargs):
        if self.write_hook is None:
            raise KeyError("write hook isn't set.")
        kwargs['service_type'] = self.type
        return self.write_hook(channel, device, _property, **kwargs)

    def _wait_for_write(self, package_id, service_type, timeout=30, poll_time=0.05):
        res = requests.get(f'http://{OBSERVER_URL}/find/{package_id}/{service_type}')
        if res.status_code == 200:
            return res.json()
        time_counter = 0.0
        while(res.status_code == 202):
            time.sleep(poll_time)
            time_counter += poll_time
            res = requests.get(f'http://{OBSERVER_URL}/find/{package_id}/{service_type}')
            if res.status_code == 200:
                _logger.debug(f"service name = {service_type}")
                return res.json()
            if time_counter >= timeout:
                _logger.error(f"timeout reached for package_id={package_id} and service_type={service_type}.")
                return None
            poll_time *= 2.0

    def sync_write(self, channel, device, _property, **kwargs):
        p_id = self.async_write(channel, device, _property, **kwargs)

        if len(self.simulations) > 0:
            for sim in self.simulations:
                res = self._wait_for_write(p_id, sim)
                if res is None:
                    raise TimeoutError(f"timeout reached for package_id={p_id} and service_type={sim}.")
        else:
            res = self._wait_for_write(p_id, MachineService.__name__)
            if res is None:
                raise TimeoutError(f"timeout reached for package_id={p_id} and service_type={MachineService.__name__}.")

    def read(self, channel, device, _property, **kwargs):
        if self.read_hook is None:
            raise KeyError("read_hook isn't set.")
        return self.read_hook(channel, device, _property, **kwargs)

    def publish_results(self, res: AgentResultMessage):
        self.producer.async_produce(AGENT_EVENTS, res.serialize(),
                                    Headers(package_id=self.current_package_id, source=self.type, msg_type=self.type))

    def reconfig_event(self, msg):
        """[summary]
        Function that can be overloaded by the concret service to reconfig without restarting
        :param msg: [description]
        :type msg: [type]
        """
        pass

    def _does_local_storage_exists(self):
        # ToDo: Not implemented yet
        return False

    def post_init(self):
        for msg in consume([SERVICE_INPUT_TOPIC, RECONFIG_TOPIC], timeout_poll=0.1, group_id=self.type, bootstrap_server=KAFKA_SERVER_URL):
            self.service_input_handler(msg)

    def _service_input_event_handler(self, msg):
        data = SimpleServiceMessage.deserialize([msg])
        result = self.proposal(data.params)
        # store message
        if result != None:
            agent_result, error_code, error_message = result
            if self._does_local_storage_exists():
                # TODO: store the agent_result in local db and set agent_result to db url
                pass
            self.producer.async_produce(AGENT_EVENTS, AgentResultMessage(agent_result, error_message, error_code).serialize(),
                                        Headers(package_id=self.current_package_id, source=self.type, msg_type=self.type))
            _logger.debug(f"send result message to topic '{AGENT_EVENTS}'")

        data = SetMachineMessage(is_last_message=True, write_commands=[])
        self.producer.sync_produce(MACHINE_INPUT_TOPIC, data.serialize(), Headers(package_id=self.current_package_id, source=self.type, msg_type=self.type))
        _logger.debug("send last message.")

    def service_input_handler(self, msg, **kwargs):
        timestamp_type, timestamp = msg.timestamp()
        if timestamp_type == TIMESTAMP_NOT_AVAILABLE:
            _logger.debug(f"[{self.name}] receive a message without a timestamp")
            return
        headers = Headers.from_kafka_headers(msg.headers())
        self.current_package_id = headers.package_id
        #self.machine_adapter.active_package_id = headers.package_id
        _logger.debug(f'[{self.name}] call service_input_handler receive headers: {str(headers)} group_id: {",".join([t.group_id for t in self.thread_pool])}')
        _logger.debug(f"Received message from topic '{msg.topic()}'")

        if headers.is_message_for(self.type) or headers.is_message_for(self.name):
            if msg.topic() == SERVICE_INPUT_TOPIC:
                self._service_input_event_handler(msg)

            elif msg.topic() == RECONFIG_TOPIC:
                _logger.debug(f"reconfig message received")
                self.reconfig_event(json.loads(msg.value().decode('utf-8')))
                return

        _logger.debug(f'[{self.name}] end service_input_handler')
