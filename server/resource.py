import falcon
import json

class Resource(object):
    def _get_parts(self, string):
        if string[0] == '$':
            return string[1:].split('.')
        else:
            return string.split('.')

class ActionResource(Resource):
    def __init__(self, engines):
        self.engines = engines

    def on_post(self, req, resp, **kwargs):
        engine = self.engines.get(kwargs['engine_id'])
        action = kwargs['action_id']
        res = engine.run_action(action)

class ModuleResource(Resource):
    def __init__(self, db, engines):
        self.db = db
        self.engines = engines

    def on_get(self, req, resp, **kwargs):
        modules = self.db.get_all()
        calc_mods = [self._populate_module(m) for m in modules]

        req.context['result'] = calc_mods

    def _populate_module(self, module):
        populated = {k: self._populate_field(v) for k, v in module.items()}
        return populated

    def _populate_field(self, field):
        if type(field) is str and len(field) > 0 and field[0] == '$':
            return self._get_field(field)
        else:
            return field

    def _get_field(self, field):
        parts = self._get_parts(field)
        engine = self.engines.get(parts[0])
        response = engine.get_property(parts[1])
        if response.is_success():
            return response.message
        else:
            return 'Unknown'
