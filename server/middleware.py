import falcon
import json

class Middleware(object):
    def __init__(self):
        super(Middleware, self).__init__()

    def process_request(self, req, resp):
        pass
    def process_resource(self, req, resp, resource):
        pass
    def process_response(self, req, resp, resource):
        pass

class LogMiddleware(Middleware):
    def process_request(self, req, resp):
        print(req)

class JSONTranslatorMiddleware(Middleware):
    def process_response(self, req, resp, resource):
        if 'result' not in req.context:
            return
        resp.body = json.dumps(req.context['result'])

class AuthMiddleware(Middleware):
    def __init__(self, apikeys):
        super(AuthMiddleware, self).__init__()
        self.keys = apikeys

    def process_request(self, req, resp):
        if req.method not in ('OPTIONS'):
            token = req.get_header('X-Api-Key')
            if token is None:
                raise falcon.HTTPUnauthorized('Auth token required',
                    'Please provide an auth token as part of the request.')
            if not self._token_is_valid(token):
                raise falcon.HTTPUnauthorized('Authentication required',
                    'The provided auth token is not valid.')

    def _token_is_valid(self, token):
        return token in self.keys

class CorsMiddleware(Middleware):
    def process_response(self, req, resp, resource):
        origin = req.get_header('Origin')
        resp.set_header(
            'Access-Control-Allow-Origin',
            '*'
        )
        resp.set_header(
            'Access-Control-Allow-Headers',
            'Content-Type, X-Api-Key'
        )
