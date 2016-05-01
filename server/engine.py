import falcon

import socket
import struct
import threading

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

class Engine(object):

    def __init__(self, props, config):
        self.props = props
        self.config = config

    def run_action(self, action_name):
        return engine.EngineResponse(
            engine.EngineResponse.ERROR, 'Function not implemented')

    def get_property(self, property_name):
        return engine.EngineResponse(
            engine.EngineResponse.ERROR, 'Function not implemented')

    def _get_plain_property(self, property_name):
        return engine.EngineResponse(
            engine.EngineResponse.ERROR, 'Function not implemented')

    def _get_calculated_property(self, property_name):
        return engine.EngineResponse(
            engine.EngineResponse.ERROR, 'Function not implemented')

    def _run_plain_action(self, action_name):
        return engine.EngineResponse(
            engine.EngineResponse.ERROR, 'Function not implemented')

    def _run_calculated_action(self, action_name):
        return engine.EngineResponse(
            engine.EngineResponse.ERROR, 'Function not implemented')

    def _success(self, msg):
        return EngineResponse(EngineResponse.SUCCESS, msg)

    def _error(self, msg):
        return EngineResponse(EngineResponse.ERROR, msg)
