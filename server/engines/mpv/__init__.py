import json

from server import engine
from .config import commands, calculated_commands, props, calculated_props

class MpvEngine(engine.Engine, engine.SocketMixin):
    def __init__(self, args):
        config = engine.EngineConfiguration(
            args, commands, calculated_commands, props, calculated_props
        )
        super(MpvEngine, self).__init__(args, config)

    def _get_plain_property(self, command):
        resp = self.send_command(command)
        if resp.message:
            msg = resp.message.get('data', None)
        else:
            msg = None
        return engine.EngineResponse(resp.status, msg)

    def _send_action_command(self, command):
        return self.send_command(command)

    def send_command(self, cmd):
        data = self._pack_command(cmd)
        res, data = self._send(data, self.args.get('socket', None))
        r = engine.EngineResponse.SUCCESS if res == 'success' else engine.EngineResponse.ERROR
        return engine.EngineResponse(r, data)

    def _pack_command(self, command):
        ''' Packs command in json format that mpv understands'''
        ret = {}
        ret['command'] = command
        data = json.dumps(ret, separators=",:")
        return data.encode("utf8", "strict") + b"\n"
