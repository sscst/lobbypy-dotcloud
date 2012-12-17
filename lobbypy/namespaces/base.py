from socketio.namespace import BaseNamespace as Namespace
from lobbypy import app

class BaseNamespace(Namespace):
    def __init__(self, *args, **kwargs):
        request = kwargs.get('request', None)
        super(BaseNamespace, self).__init__(*args, **kwargs)
        if request:
            self.ctx = app.request_context(request.environ)
            self.ctx.push()
            app.preprocess_request()
            self.request = self.ctx.request

    def disconnect(self, *args, **kwargs):
        super(BaseNamespace, self).disconnect(*args, **kwargs)
        self.ctx.pop()
