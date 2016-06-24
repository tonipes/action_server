import falcon
import json
import copy
from .engine import EngineException

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
        if not engine:
            resp.status = falcon.HTTP_404
            req.context['result'] = "Engine not found"
        else:
            try:
                res = engine.run_action(kwargs['action_id'])
                req.context['result'] = res.message
                resp.status = res.status
            except EngineException as e:
                resp.status = '569 Engine Error'
                req.context['result'] = str(e)

class PropertyResource(Resource):
    def __init__(self, engines):
        self.engines = engines

    def on_get(self, req, resp, **kwargs):
        ''' Get property value '''
        engine = self.engines.get(kwargs['engine_id'])
        if not engine:
            resp.status = falcon.HTTP_404
            req.context['result'] = "Engine not found"
        else:
            try:
                res = engine.get_prop_value(kwargs['prop_id'])
                req.context['result'] = res.message
                resp.status = res.status
            except EngineException as e:
                resp.status = '569 Engine Error'
                req.context['result'] = str(e)

class ModuleResource(Resource):
    def __init__(self, db, engines):
        self.db = db
        self.engines = engines

    def on_get(self, req, resp, **kwargs):
        ''' Get all modules and their states '''
        path = kwargs.get('path', [])
        tree = self.db.get_from(path)
        if not tree:
            resp.status = falcon.HTTP_404
            req.context['result'] = "Item not found"
        else:
            try:
                populated = self._populate_item(tree)
                req.context['result'] = populated
            except EngineException as e:
                resp.status = '569 Engine Error'
                req.context['result'] = str(e)


    def _populate_item(self, item):
        ''' Populates item tree recursively '''
        if type(item) == list:
            res = [None] * len(item)
            for i, e in enumerate(item):
                res[i] = (self._populate_item(e))
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
        response = engine.get_prop_value(parts[1])

        if response.message:
            return response.message
        else:
            return 'Unknown'
