import falcon

class Sink(object):
    def __init__(self, module_res):
        self.module_res = module_res

    def get_sink(self, req, resp):
        if req.method != 'GET':
            return falcon.HTTPMethodNotAllowed('GET')
        parts = req.path.split('/')[1:]

        return self.module_res.on_get(req, resp, path=parts)
