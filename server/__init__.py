import falcon
from wsgiref import simple_server

from .server_components import JSONTranslator
from .server_components import ActionListResource
from .server_components import ActionDetailResource
from .server_components import ActionStorage
from .server_components import EngineStorage
from .server_components import AuthMiddleware

from .engines.mpv import MpvEngine
from .engines.script import ScriptEngine
from .engines.media_key import MediaKeyEngine

class Server(object):
    def __init__(self, config, action_data):
        self.app = falcon.API(middleware=[
            AuthMiddleware(config['api_keys']),
            JSONTranslator()
        ])

        engine_config = config.get('engine_config', None)

        self.engines = {
            'mpv': MpvEngine(engine_config.get('mpv', None)),
            'script': ScriptEngine(engine_config.get('script', None)),
            'media_key': MediaKeyEngine(engine_config.get('media_key', None)),
        }
        db = ActionStorage(action_data)
        engine_storage = EngineStorage(self.engines)

        action_res = ActionDetailResource(db, engine_storage)
        action_list = ActionListResource(db)

        self.app.add_route('/actions', action_list)
        self.app.add_route('/actions/{action_id}', action_res)

        self.httpd = simple_server.make_server(
            config['address'], config['port'], self.app)


    def start(self):
        self.httpd.serve_forever()

    def stop(self):
        print("stopping server")
        pass

# def run_server(config, action_data):
#     app = falcon.API(middleware=[
#         AuthMiddleware(config['api_keys']),
#         JSONTranslator()
#     ])
#
#     engine_config = config.get('engine_config', None)
#
#     engines = {
#         'mpv': MpvEngine(engine_config.get('mpv', None)),
#         'script': ScriptEngine(engine_config.get('script', None)),
#         'media_key': MediaKeyEngine(engine_config.get('media_key', None)),
#     }
#
#     db = ActionStorage(action_data)
#     engine_storage = EngineStorage(engines)
#
#     action_res = ActionDetailResource(db, engine_storage)
#     action_list = ActionListResource(db)
#
#     app.add_route('/actions', action_list)
#     app.add_route('/actions/{action_id}', action_res)
#
#     httpd = simple_server.make_server(config['address'], config['port'], app)
#     httpd.serve_forever()
