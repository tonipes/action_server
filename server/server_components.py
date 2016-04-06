import falcon
import uuid
import json

class Resource(object):
    exclude_fields = []

    def __init__(self, db):
        self.db = db

    def get_items(self, **kwargs):
        pass

    def on_get(self, req, resp, **kwargs):
        got = self.get_items(**kwargs)
        items = [self.get_fields(item) for item in got]
        items = items[0] if len(items) == 1 else items
        resp.status = falcon.HTTP_200
        req.context['result'] = items

    def get_fields(self, item):
        ret = {}
        for key, val in item.items():
            if not key in self.exclude_fields:
                ret[key] = val
        return ret

class JSONTranslator(object):
    def process_response(self, req, resp, resource):
        if 'result' not in req.context:
            return
        resp.body = json.dumps(req.context['result'])

class ActionStorage(object):
    last_id = 0

    def __init__(self, action_data):
        def get_item_key_pair(action):
            key = self.get_new_id()
            action['id'] = key
            return (key, action)

        paired = [get_item_key_pair(act) for act in action_data]
        self.actions = dict(paired)

    def get_all(self):
        return [value for key,value in self.actions.items()]

    def get(self, id):
        try:
            action = self.actions[id]
        except KeyError:
            raise falcon.HTTPNotFound()
        return action

    def get_new_id(self):
        self.last_id = self.last_id +1
        return str(self.last_id)
        # return str(uuid.uuid4())[:8]

class EngineStorage(object):
    def __init__(self, engines):
        self.engines = engines

    def get(self, id):
        try:
            action = self.engines[id]
        except KeyError:
            raise falcon.HTTPNotFound()
        return action

class AuthMiddleware(object):
    def __init__(self, apikeys):
        self.keys = apikeys

    def process_request(self, req, resp):
        token = req.get_header('X-Auth-Token')

        if token is None:
            raise falcon.HTTPUnauthorized('Auth token required',
                'Please provide an auth token as part of the request.')

        if not self._token_is_valid(token):
            raise falcon.HTTPUnauthorized('Authentication required',
                'The provided auth token is not valid.')

    def _token_is_valid(self, token):
        return token in self.keys

class ActionResourse(Resource):
    exclude_fields = []

class ActionListResource(ActionResourse):
    def get_items(self, **kwargs):
        return self.db.get_all()

class ActionDetailResource(ActionResourse):
    def __init__(self, db, engines):
        super(ActionDetailResource, self).__init__(db)
        self.engines = engines

    def get_items(self, **kwargs):
        item_id = kwargs["action_id"]
        return [self.db.get(item_id)]

    def on_post(self, req, resp, **kwargs):
        action = self.get_items(**kwargs)[0]
        engine = self.engines.get(action['engine'])
        result = engine.run_action(action)
        resp.status = result[1]
        resp.body = result[0]
