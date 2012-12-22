from socketio.namespace import BaseNamespace as Namespace
import redis
from json import dumps, loads
from flask import current_app

class BaseNamespace(Namespace):
    def __init__(self, *args, **kwargs):
        request = kwargs.get('request', None)
        if request:
            self.ctx = current_app.request_context(request.environ)
            self.ctx.push()
            current_app.preprocess_request()
            del kwargs['request']
        super(BaseNamespace, self).__init__(*args, **kwargs)

    def disconnect(self, *args, **kwargs):
        self.ctx.pop()
        super(BaseNamespace, self).disconnect(*args, **kwargs)

class RedisBroadcastMixin(object):
    def broadcast_event(self, ns, event, *args):
        r = redis.Redis()
        r.publish(ns, dumps(dict(event=event, args=args)))

class RedisListenerMixin(object):
    def listener(self, ns):
        r = redis.StrictRedis()
        r = r.pubsub()

        r.subscribe(ns)

        for m in r.listen():
            if m['type'] == 'message':
                data = loads(m['data'])
                event = data.pop('event')
                method_name = 'on_redis_%s' % event
                args = data.pop('args', [])
                self.call_method(method_name, None, *args)
