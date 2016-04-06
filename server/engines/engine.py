import falcon

import socket
import struct
import threading
import Queue

ACT_OK = ('Action successful.', falcon.HTTP_200)
ACT_FAIL = ('Action failed.', falcon.HTTP_503)
EGN_NOT_ABLE = ('Engine not able to run action.', falcon.HTTP_503)

class Engine(object):

    def __init__(self, config):
        self.config = config

    def run_action(self, action):
        pass
