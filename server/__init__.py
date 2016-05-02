import yaml
import falcon

from . import middleware
from . import resource
from . import storage

from .engines.mpv import MpvEngine
from .engines.cmus import CmusEngine

def get_config(filename):
    with open(filename, 'r') as f:
        return yaml.load(f)

config = get_config('config_server.yml')
modules = get_config('config_modules.yml')

app = falcon.API(middleware=[
    # middleware.CorsMiddleware(), # Probably not needed anymore
    middleware.AuthMiddleware(config['api_keys']),
    middleware.JSONTranslatorMiddleware()
])

engine_config = config.get('engine_config', None)

engines = {
    'mpv': MpvEngine(engine_config.get('mpv', None)),
    'cmus': CmusEngine(engine_config.get('cmus', None)),
}

db = storage.ActionStorage(modules)
engine_storage = storage.EngineStorage(engines)

module_res = resource.ModuleResource(db, engines)
module_run = resource.ActionResource(engines)

app.add_route('/modules', module_res)
app.add_route('/action/{engine_id}/{action_id}', module_run)
