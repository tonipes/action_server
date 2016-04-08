import socket
import threading
import time
import json
import falcon
import select

from . import engine

class MpvEngine(engine.Engine):
    def __init__(self, config):
        super(MpvEngine, self).__init__(config)
        self.socket_path = config.get('socket', None)

    def receive(self, sock):
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

    def pack_command(self, command):
        ret = {}
        ret['command'] = command
        data = json.dumps(ret, separators=",:")
        return data.encode("utf8", "strict") + b"\n"

    def run_action(self, action):
            parameters = action['parameters']
            command = parameters.get('command', None)
            data = self.pack_command(command)
            # TODO: Do not create new socket for each action
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            try:
                sock.connect(self.socket_path)
                sock.sendall(data)
                result = self.receive(sock)
                sock.close()
            except IOError as e:
                print(str(e))
                return self.error_msg(str(e))
            return self.success_msg(result)
