import socket
import threading
import time
import json
import falcon
import select
import json
from server import engine
from .config import config

class SocketResponse(engine.EngineResponse):
    def is_success(self):
        sp = super(SocketResponse, self).is_success()
        if 'error' in self.message:
            return sp and self.message['error'] == 'success'
        else:
            # Sometimes there is no error key in response.
            # It happens when seeking and seeking is not ready when response is sent
            # We don't care about seek still going on, it is still a success.
            return sp

class MpvEngine(engine.Engine):
    def __init__(self, props):
        super(MpvEngine, self).__init__(props, config)
        self.socket_path = props.get('socket', None)

    def get_property(self, property_name):
        if property_name in self.config['properties']:
            res = self._get_plain_property(property_name)

        elif property_name in self.config['calculated_props']:
            res = self._get_calculated_property(property_name)

        else:
            res = engine.EngineResponse(
                engine.EngineResponse.ERROR, 'Property not found')

        return res

    def _get_plain_property(self, property_name):
        prop = self.config['properties'][property_name]
        data = self._pack_command(prop)
        res = self._send(data)

        if res.is_success():
            return engine.EngineResponse(
                engine.EngineResponse.SUCCESS, res.message.get('data', None))
        else:
            return engine.EngineResponse(
                engine.EngineResponse.ERROR, '')

    def _get_calculated_property(self, property_name):
        prop = self.config['calculated_props'][property_name]
        child_props_names = prop[0]
        func = prop[1]
        child_props = [self.get_property(n).message for n in child_props_names]

        try:
            res = func(*child_props)
        except:
            return engine.EngineResponse(
                engine.EngineResponse.ERROR, 'Calc error')
        return engine.EngineResponse(
            engine.EngineResponse.SUCCESS, res)

    def run_action(self, action_name):
        if action_name in self.config['actions']:
            command = self.config['actions'][action_name]
            res = self._send_action(command)

        elif action_name in self.config['calculated_actions']:
            response = self._get_calculated_command(action_name)
            res = self._send_action(response.message)
        else:
            res = engine.EngineResponse(
                engine.EngineResponse.ERROR, 'Action not found')
        return res

    def _get_calculated_command(self, action_name):
        prop = self.config['calculated_actions'][action_name]
        child_props_names = prop[0]
        func = prop[1]
        child_props = [self.get_property(n).message for n in child_props_names]
        try:
            res = func(*child_props)
        except:
            return engine.EngineResponse(
                engine.EngineResponse.ERROR, 'Calc error')
        return engine.EngineResponse(
            engine.EngineResponse.SUCCESS, res)

    def _send_action(self, command):
        data = self._pack_command(command)
        res = self._send(data)
        return res

    def _send(self, data):
        # TODO: Do not create new socket for each action
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            sock.connect(self.socket_path)
            sock.sendall(data)
            result = self._receive(sock)
            sock.close()
        except IOError as e:
            print(str(e))
            return SocketResponse(SocketResponse.ERROR, str(e))
        return SocketResponse(SocketResponse.SUCCESS, json.loads(result))

    def _receive(self, sock):
        data = b""
        part = b""
        done = False
        while not done:
            r, w, e = select.select([sock], [], [], 1)
            if r:
                part = sock.recv(1)
                if not part:
                    done = True
                if not len(part) > 0:
                    done = True
                if part == b"\n":
                    done = True
                data += part
            else:
                done = True
        return data.decode('utf-8')

    def _pack_command(self, command):
        ret = {}
        ret['command'] = command
        data = json.dumps(ret, separators=",:")
        return data.encode("utf8", "strict") + b"\n"
