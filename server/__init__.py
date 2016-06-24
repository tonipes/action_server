import yaml
import falcon

from . import middleware
from . import resource
from . import storage

from .engines.mpv import MpvEngine
from .engines.cmus import CmusEngine
from .sink import Sink

def get_config(filename):
    with open(filename, 'r') as f:
        return yaml.load(f)

config = get_config('config_server.yml')
modules = get_config('config_modules.yml')

app = falcon.API(middleware=[
    middleware.AuthMiddleware(config['api_keys']),
    middleware.JSONTranslatorMiddleware()
])

engine_config = config.get('engine_config', None)

engines = {
    'mpv': MpvEngine(engine_config.get('mpv', None)),
    # 'cmus': CmusEngine(engine_config.get('cmus', None)),
}

module_db = storage.ModuleStorage(modules)
engine_db = storage.EngineStorage(engines)

module_res = resource.ModuleResource(module_db, engine_db)
action_res = resource.ActionResource(engine_db)
prop_res = resource.PropertyResource(engine_db)

sink = Sink(module_res)
app.add_sink(sink.get_sink, '/')

app.add_route('/action/{engine_id}/{action_id}', action_res)
app.add_route('/prop/{engine_id}/{prop_id}', prop_res)
