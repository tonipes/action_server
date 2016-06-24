import falcon

import socket
import struct
import threading
import select
import json

class EngineItem(object):
    def __init__(self, args=None, deps=[], fn=None):
        self.args = args
        self.deps = deps
        self.fn = fn

    def get_deps(self, engine):
        return [engine.config.get_prop(d).get(engine) for d in self.deps]

class EngineProp(EngineItem):
    def get(self, engine):
        if self.fn:
            calc_deps = self.get_deps(engine)
            try:
                calc_value = self.fn(*calc_deps)
            except Exception as e:
                raise EngineException("Error calculating property value. " + str(e))
        else:
            calc_value = engine._calc_prop_value(self.args)

        return calc_value

class EngineAction(EngineItem):
    def run(self, engine):
        if self.fn:
            calc_deps = self.get_deps(engine)
            try:
                cmd = self.fn(*calc_deps)
            except Exception as e:
                raise EngineException("Error calculating command value." + str(e))
        else:
            cmd = self.args

        return engine._run_command(cmd)

class EngineException(Exception):
    pass

class EngineResponse(object):

    def __init__(self, status, msg):
        self.status = status
        self.message = msg

    def __str__(self):
        return '<' + str(self.status) + ' - ' + str(self.message) + '>'

class EngineConfig(object):
    def __init__(self, props, actions):
        self.props = props
        self.actions = actions

    def get_action(self, name):
        if name in self.actions:
            return self.actions[name]
        else:
            raise KeyError('No action found: ' + name)

    def get_prop(self, name):
        if name in self.props:
            return self.props[name]
        else:
            raise KeyError('No prop found: ' + name)

class Engine(object):
    def __init__(self, args, config):
        self.args = args
        self.config = config

    def get_prop_value(self, name):
        try:
            prop = self.config.get_prop(name)
        except KeyError as e:
            return EngineResponse(falcon.HTTP_404, str(e))
        try:
            res = prop.get(self)
            return EngineResponse(falcon.HTTP_200, res)
        except EngineException as e:
            return EngineResponse(falcon.HTTP_200, 'Unknown') # ???

    def run_action(self, name):
        try:
            action = self.config.get_action(name)
        except KeyError as e:
            return EngineResponse(falcon.HTTP_404, str(e))
        res = action.run(self)
        return EngineResponse(falcon.HTTP_200, res)

    def _calc_prop_value(self, args):
        pass

    def _run_command(self, cmd):
        pass

class EngineSocketError(Exception):
    def __init__(self, msg):
        super(EngineSocketError, self).__init__(msg)

class SocketEngine(Engine):
    def __init__(self, args, config):
        super(SocketEngine, self).__init__(args, config)
        self.socket_path = self.args.get('socket', '')

    def _connect(self):
        try:
            self._socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self._socket.connect(self.socket_path)
        except socket.error as e:
            if e.errno == 2:
                raise EngineSocketError(
                    'No such file or directory: \'%s\'' % self.socket_path)
            raise e

    def _disconnect(self):
        self._socket.close()

    def _reconnect(self):
        self._disconnect()
        self._connect()

    def _send(self, cmd, buf=4096):
        try:
            self._socket.send(cmd)
            return self._socket.recv(buf)
        except socket.error as e:
            if e.errno == 32:
                raise EngineSocketError('Broken pipe')
            elif e.errno == 107:
                raise EngineSocketError(
                    'Transport endpoint is not connected')
            raise e

    def __del__(self):
        self._disconnect()
