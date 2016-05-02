import json

from server import engine
from .config import commands, calculated_commands, props, calculated_props

class MpvEngine(engine.SocketEngine):
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
        self._connect()
        res = self._send(self._pack_command(cmd))
        result_data = self._unpack_result(res)
        # TODO Actually figure out if success or not
        return engine.EngineResponse(engine.EngineResponse.SUCCESS, result_data)

    def _pack_command(self, command):
        ''' Packs command in json format that mpv understands'''
        ret = {}
        ret['command'] = command
        data = json.dumps(ret, separators=",:")
        return data.encode("utf8", "strict") + b"\n"

    def _unpack_result(self, result):
        if result:
            decoded = result.decode('utf-8')
            # There might be multiple json enties
            # We only need the first one
            parts = decoded.split('\n')
            json_data = json.loads(parts[0])
            return json_data
        else:
            return None
