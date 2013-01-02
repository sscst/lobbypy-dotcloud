from gevent import monkey; monkey.patch_all()
import os, sys
from flask.ext.script import Manager, prompt_bool
from socketio.server import SocketIOServer

from lobbypy import create_app, config_app

app = create_app()
manager = Manager(app)
# Bind to PORT if defined, otherwise default to 5000.
port = int(os.environ.get('PORT', 5000))

@manager.option('--no-rcon-check', dest='rcon_check', action='store_const',
        const=True, default=False)
@manager.option('--debug', dest='debug', action='store_const', const=True, default=False)
def run(debug, rcon_check):
    from random import randint
    from asciiart import images, title
    sys.stderr.write(images[randint(0, len(images) - 1)] + '\n')
    sys.stderr.write(title + '\n')
    config_app(app, DEBUG=debug, RCON_CHECK_SERVER=not rcon_check)
    SocketIOServer(('', port), app, resource="socket.io").serve_forever()

@manager.command
def init_db():
    config_app(app)
    from lobbypy.utils import db
    db.create_all()

@manager.command
def drop_db():
    config_app(app)
    from lobbypy.utils import db
    if prompt_bool(
            "Are you sure you want to clear the database"):
        db.drop_all()

if __name__ == '__main__':
    manager.run()
