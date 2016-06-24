import json
import re
import socket
from server import engine
from .config import commands, calculated_commands, props, calculated_props

class regex:
    status = r'(tag|set)? ?(\w+) (.*)\n'
    playing = r'^status playing\n(.*)'
    paused = r'^status paused\n(.*)'
    stopped = r'^status stopped\n(.*)'
    paused_or_stopped = r'^status (paused|stopped)\n(.*)'

class CmusEngine(engine.SocketEngine):
    def __init__(self, args):
        config = engine.EngineConfiguration(
            args, commands, calculated_commands, props, calculated_props
        )
        super(CmusEngine, self).__init__(args, config)

    def _get_plain_property(self, command):
        props = self._get_props()
        value = props[command]
        return engine.EngineResponse(engine.EngineResponse.SUCCESS, value)

    def _get_props(self):
        self._connect()
        res = self._send(self._pack_command('status'))
        status = self._unpack_result(res)
        ret = re.findall(regex.status, status, re.MULTILINE)
        ret = {i[1]: i[2] for i in ret}

        for k, v in ret.items():
            if k in ['artist', 'album', 'comment', 'date', 'genre']:
                continue

            if v == 'true':
                ret[k] = True
            elif v == 'false':
                ret[k] = False
            else:
                try:
                    ret[k] = int(v)
                    continue
                except ValueError:
                    pass

                try:
                    ret[k] = float(v)
                    continue
                except ValueError:
                    pass

        return ret

    def _send_action_command(self, command):
        try:
            self._connect()
            res = self._send(self._pack_command(command))
        except Exception as e:
            return engine.EngineResponse(engine.EngineResponse.ERROR, str(e))
        # TODO: Figure out if actually success or not
        return engine.EngineResponse(engine.EngineResponse.SUCCESS, str(res))

    def _unpack_result(self, res):
        return res.decode("utf8")

    def _pack_command(self, cmd):
        return ('%s\n' % cmd).encode("utf8")
