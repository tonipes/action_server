import falcon

import socket
import struct
import threading
import select
import json

class EngineResponse(object):
    SUCCESS = 0
    ERROR = 1

    def __init__(self, status, msg):
        self.status = status
        self.message = msg

    def is_success(self):
        return self.status == EngineResponse.SUCCESS

    def __str__(self):
        st = 'Success' if self.is_success() else 'Error'
        return '<' + st + ' - ' +str(self.message) + '>'

class EngineConfiguration(object):
    def __init__(self, args, action_plain, action_calc, prop_plain, prop_calc):
        self.args = args
        self.action_plain = action_plain
        self.action_calc = action_calc
        self.prop_plain = prop_plain
        self.prop_calc = prop_calc

    def get_action(self, name):
        if name in self.action_plain:
            return self.action_plain[name]
        elif name in self.action_calc:
            return self.action_calc[name]
        else:
            return None

    def get_property(self, name):
        if name in self.prop_plain:
            return self.prop_plain[name]
        elif name in self.prop_calc:
            return self.prop_calc[name]
        else:
            return None

    def is_calculated_action(self, name):
        return name in self.action_calc

    def is_plain_action(self, name):
        return name in self.action_plain

    def is_calculated_property(self, name):
        return name in self.prop_calc

    def is_plain_property(self, name):
        return name in self.prop_plain

class Engine(object):

    def __init__(self, args, config):
        self.args = args
        self.config = config

    def get_property(self, property_name):
        ''' Gets property. Returns EngineResponse '''
        prop_cmd = self.config.get_property(property_name)

        if self.config.is_calculated_property(property_name):
            response = self._get_calculated_property(prop_cmd)
        elif self.config.is_plain_property(property_name):
            response = self._get_plain_property(prop_cmd)
        else:
            pass
        return response

    def _get_calculated_property(self, prop):
        ''' Gets calculated property. Returns EngineResponse '''
        child_props_names = prop[0]
        func = prop[1]
        child_props = [self.get_property(n).message for n in child_props_names]

        try:
            res = func(*child_props)
        except:
            return EngineResponse(EngineResponse.ERROR, 'Property calculation error')
        return EngineResponse(EngineResponse.SUCCESS, res)

    def run_action(self, action_name):
        ''' Runs action. Returns EngineResponse '''
        prop_cmd = self.config.get_action(action_name)

        if self.config.is_calculated_action(action_name):
            command = self._get_calculated_action_command(prop_cmd)
        elif self.config.is_plain_action(action_name):
            command = prop_cmd
        else:
            pass
        return self._send_action_command(command)

    def _get_calculated_action_command(self, action):
        child_props_names = action[0]
        func = action[1]
        child_props = [self.get_property(n).message for n in child_props_names]

        try:
            return func(*child_props)
        except:
            return None

    def _send_action_command(self, command):
        pass

    def _get_plain_property(self, prop_cmd):
        ''' Gets plain property. Returns EngineResponse '''
        pass

    def _success(self, msg):
        return EngineResponse(EngineResponse.SUCCESS, msg)

    def _error(self, msg):
        return EngineResponse(EngineResponse.ERROR, msg)

class SocketMixin(object):

    def _send(self, data, path):
        # TODO: Do not create new socket for each action
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            sock.connect(path)
            sock.sendall(data)
            result = self._receive(sock)
            sock.close()
        except IOError as e:
            return ('error', None)
        return ('success', json.loads(result))

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
