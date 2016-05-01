import json

from server import engine
from .config import commands, calculated_commands, props, calculated_props

class CmusEngine(engine.Engine, engine.SocketMixin):
    def __init__(self, args):
        config = engine.EngineConfiguration(
            args, commands, calculated_commands, props, calculated_props
        )
        super(CmusEngine, self).__init__(args, config)

    def _get_plain_property(self, command):
        pass

    def _send_action_command(self, command):
        pass
