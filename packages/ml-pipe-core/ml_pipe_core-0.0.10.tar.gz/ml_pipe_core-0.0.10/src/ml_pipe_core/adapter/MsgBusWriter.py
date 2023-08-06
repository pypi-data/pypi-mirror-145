from ..simulation.update_message_types import WriteCommand, SetMachineMessage
from ..machine_topics import MACHINE_INPUT_TOPIC
from ..message import Headers
from ..logger import init_logger
from ..event_utls.producer import Producer
from ..utils.utils import generate_unique_id

_logger = init_logger(__name__)


class MessageBusWriter:
    def __init__(self, producer=None):
        self.producer = Producer() if producer is None else producer

    def __call__(self, channel, device, _property, **kwargs):
        s_type = kwargs.get("service_type")
        if s_type is None:
            _logger.error("service_type isn't set.")
            return
        data = SetMachineMessage(is_last_message=False, write_commands=[WriteCommand(channel=channel, device_name=device, property=_property, params=kwargs)])
        package_id = generate_unique_id()
        self.producer.sync_produce(MACHINE_INPUT_TOPIC, data.serialize(), Headers(package_id=package_id, source=s_type, msg_type=s_type))
        return package_id
