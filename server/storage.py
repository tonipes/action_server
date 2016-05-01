import falcon
import uuid

class ActionStorage(object):
    last_id = 0

    def __init__(self, modules):
        def get_item_key_pair(action):
            key = self.get_new_id()
            action['id'] = key
            return (key, action)

        paired = [get_item_key_pair(module) for module in modules]
        self.modules = dict(paired)

    def get_all(self):
        return [value for key,value in self.modules.items()]

    def get(self, id):
        try:
            module = self.modules[id]
        except KeyError:
            raise falcon.HTTPNotFound()
        return module

    def get_new_id(self):
        self.last_id = self.last_id + 1
        return str(self.last_id)
        # return str(uuid.uuid4())[:8]

class EngineStorage(object):
    def __init__(self, engines):
        self.engines = engines

    def get(self, id):
        try:
            engine = self.engines[id]
        except KeyError:
            raise falcon.HTTPNotFound()
        return engine
