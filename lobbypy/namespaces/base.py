from socketio.namespace import BaseNamespace as Namespace
from lobbypy import app

class BaseNamespace(Namespace):
    def initialize(self):
        request = self.request
        self.ctx = app.request_context(request.environ)
        self.ctx.push()
        app.preprocess_request()
        self.request = self.ctx.request

    def disconnect(self, *args, **kwargs):
        super(BaseNamespace, self).disconnect(*args, **kwargs)
        self.ctx.pop()
