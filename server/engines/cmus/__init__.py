import json
import socket
from server import engine
from .config import commands, calculated_commands, props, calculated_props

class CmusEngine(engine.SocketEngine):
    def __init__(self, args):
        config = engine.EngineConfiguration(
            args, commands, calculated_commands, props, calculated_props
        )
        super(CmusEngine, self).__init__(args, config)

    def _get_plain_property(self, command):
        pass

    def _send_action_command(self, command):
        self._connect()
        res = self._send(self._pack_command(command))
        # TODO: Figure out if actually success or not
        return engine.EngineResponse(engine.EngineResponse.SUCCESS, str(res))

    def _pack_command(self, cmd):
        return ('%s\n' % cmd).encode("utf8")
