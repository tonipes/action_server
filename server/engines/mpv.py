import socket
import threading
import time
import json
import falcon

import engine

class MpvEngine(engine.Engine):
    def __init__(self, config):
        super(MpvEngine, self).__init__(config)
        socket_filename = config.get('socket', None)

        self.connected = False

        self.socket_thread = threading.Thread(
            target=self.connect, args=(socket_filename, ))
        # self.socket_thread.daemon = True
        self.socket_thread.start()

    def connect(self, socket_path):
        while True:
            time.sleep(0.2)
            try:
                self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                self.socket.connect(socket_path)
            except (FileNotFoundError, ConnectionRefusedError):
                if self.connected:
                    print("Connection lost")
                self.connected = False
            else:
                if not self.connected:
                    print("Connection succesfull")
                self.connected = True

    def send(self, data):
        self.socket.send(data)

    def pack_command(self, command):
        ret = {}
        ret['command'] = command
        data = json.dumps(ret, separators=",:")
        return data.encode("utf8", "strict") + b"\n"

    def run_action(self, action):
        if self.connected:
            parameters = action['parameters']
            command = parameters.get('command', None)
            data = self.pack_command(command)
            self.send(data)
            return engine.ACT_OK
        else:
            return engine.EGN_NOT_ABLE
