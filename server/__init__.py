import yaml
import falcon

# from .server_components import JSONTranslatorMiddleware
# from .server_components import ActionListResource
# from .server_components import ActionDetailResource
# from .server_components import ActionStorage
# from .server_components import EngineStorage
# from .server_components import AuthMiddleware
# from .server_components import CorsMiddleware
# from .server_components import LogMiddleware

from . import middleware
from . import resource
from . import storage

from .engines.mpv import MpvEngine
from .engines.script import ScriptEngine
from .engines.media_key import MediaKeyEngine

def get_config(filename):
    with open(filename, 'r') as f:
        return yaml.load(f)

config = get_config('config_server.yml')
actions = get_config('config_action.yml')

app = falcon.API(middleware=[
    # LogMiddleware(),
    middleware.CorsMiddleware(),
    middleware.AuthMiddleware(config['api_keys']),
    middleware.JSONTranslatorMiddleware()
])

engine_config = config.get('engine_config', None)

engines = {
    'mpv': MpvEngine(engine_config.get('mpv', None)),
    'script': ScriptEngine(engine_config.get('script', None)),
    'media_key': MediaKeyEngine(engine_config.get('media_key', None)),
}

db = storage.ActionStorage(actions)
engine_storage = storage.EngineStorage(engines)

action_res = resource.ActionDetailResource(db, engine_storage)
action_list = resource.ActionListResource(db)

app.add_route('/actions', action_list)
app.add_route('/actions/{action_id}', action_res)
