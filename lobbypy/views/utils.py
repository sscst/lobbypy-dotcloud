from functools import update_wrapper
from flask import (
        abort,
        request,
        current_app,
        g,
)
from flask import jsonify as _jsonify

def jsonify(status_code, *args, **kwargs):
    resp = _jsonify(*args, **kwargs)
    resp.status_code = status_code
    return resp

def admin_check(f):
    def protected(*args, **kwargs):
        if not g.player or not g.player.admin:
            current_app.logger.info('Player[%s] tried to access'
                ' protected PATH[%s], but is not an admin' % (
                    g.player.id if g.player else 'Anonymous',
                    request.path))
            abort(404)
        else:
            return f(*args, **kwargs)
    return update_wrapper(protected, f)
