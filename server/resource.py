import falcon
import json
import copy

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
        ''' Run an action '''
        engine = self.engines.get(kwargs['engine_id'])
        action = kwargs['action_id']
        res = engine.run_action(action)
        req.context['result'] = res.message

class ModuleResource(Resource):
    def __init__(self, db, engines):
        self.db = db
        self.engines = engines

    def on_get(self, req, resp, **kwargs):
        ''' Get all modules and their states '''
        modules = self.db.get_all()
        populated = self._populate_item(modules)
        req.context['result'] = populated

    def _populate_item(self, item):
        ''' Populates item tree recursively '''
        if type(item) == list:
            res = [None] * len(item)
            for i, e in enumerate(item):
                res[i] = (self._populate_item(e))
                # res.append(self._populate_item(e))
        elif type(item) == dict:
            res = {}
            for k, v in item.items():
                res[k] = self._populate_item(v)
        else:
            res = self._populate_field(item)
        return res

    def _populate_field(self, field):
        ''' Returns populated value of a field or field value if bare value '''
        if type(field) is str and len(field) > 0 and field[0] == '$':
            return self._get_field(field)
        else:
            return field

    def _get_field(self, field):
        ''' Returns value for field '''
        parts = self._get_parts(field)
        engine = self.engines.get(parts[0])
        response = engine.get_property(parts[1])

        if response.is_success():
            return response.message
        else:
            return 'Unknown'
