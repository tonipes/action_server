import json

from server import engine
from .config import props, actions

class MpvEngine(engine.SocketEngine):
    def __init__(self, args):
        config = engine.EngineConfig(props, actions)
        super(MpvEngine, self).__init__(args, config)

    def _calc_prop_value(self, args):
        res = self.send_command(args)
        return res

    def _run_command(self, cmd):
        res = self.send_command(cmd)
        return res

    def send_command(self, cmd):
        try:
            self._connect()
            res = self._send(self._pack_command(cmd))
            result_data = self._unpack_result(res)
        except Exception as e:
            raise engine.EngineException("Error sending command. " + str(e))
        # if 'error' not in result_data or 'data' not in result_data:
        #     raise engine.EngineException("Invalid response")
        # if result_data['error'] != 'success':
        #     raise engine.EngineException("Request returned error" + result_data['data'])
        return result_data['data']

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
