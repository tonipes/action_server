import falcon

import socket
import struct
import threading

class Engine(object):

    def __init__(self, config):
        self.config = config

    def run_action(self, action):
        return ('Engine not implemented', falcon.HTTP_501)

    def success_msg(self, msg):
        return (msg, falcon.HTTP_200)

    def error_msg(self, msg):
        return (msg, falcon.HTTP_503)
