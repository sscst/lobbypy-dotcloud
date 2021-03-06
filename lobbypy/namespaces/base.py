from socketio.namespace import BaseNamespace as Namespace
import redis
from json import dumps, loads
from flask import current_app, g

class BaseNamespace(Namespace):
    def __init__(self, *args, **kwargs):
        app_request = kwargs.get('request', None)
        if isinstance(app_request, tuple):
            app, request = app_request
            if request and app:
                self.ctx = app.request_context(request.environ)
                self.ctx.push()
                current_app.preprocess_request()
                del kwargs['request']
        super(BaseNamespace, self).__init__(*args, **kwargs)

    def disconnect(self, *args, **kwargs):
        self.ctx.pop()
        super(BaseNamespace, self).disconnect(*args, **kwargs)

class RedisBroadcastMixin(object):
    def broadcast_event(self, ns, event, *args):
        r = redis.Redis.from_url(current_app.config['REDIS_URI'])
        r.publish(ns, dumps(dict(event=event, args=args)))
        current_app.logger.debug(
                'Publishing event %s with args %s on namespace %s' %
                (event, args, ns))

class RedisListenerMixin(object):
    def __init__(self, *args, **kwargs):
        super(RedisListenerMixin, self).__init__(*args, **kwargs)
        self.pubsub = None

    def subscribe(self, ns):
        if not self.pubsub:
            r = redis.StrictRedis.from_url(current_app.config['REDIS_URI'])
            self.pubsub = r.pubsub()
            self.pubsub.subscribe(ns)
            self.spawn(self.listener)
        else:
            self.pubsub.subscribe(ns)
        current_app.logger.debug(
                'Player: %s subscribing to namespace: %s' % (
                    g.player.id if g.player else 'Anonymous', ns))

    def unsubscribe(self, ns):
        self.pubsub.unsubscribe(ns)

    def listener(self):
        self.ctx.push()
        current_app.logger.debug(
                'Player: %s spawning listener' % (g.player.id if
                    g.player else 'Anonymous'))
        for m in self.pubsub.listen():
            if m['type'] == 'message':
                data = loads(m['data'])
                channel = m['channel']
                event = data.pop('event')
                method_name = 'on_redis_%s' % event
                args = data.pop('args', [])
                args.insert(0, channel)
                self.call_method(method_name, None, *args)
        self.ctx.pop()
