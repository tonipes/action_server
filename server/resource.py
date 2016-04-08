import falcon

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
