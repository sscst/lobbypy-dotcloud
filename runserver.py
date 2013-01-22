from gevent import monkey; monkey.patch_all()
import os, sys, json
from pbkdf2 import crypt
from flask.ext.script import Manager, prompt_bool, prompt_pass
from socketio.server import SocketIOServer

from lobbypy import create_app, config_app

app = create_app()
manager = Manager(app)
port = int(os.environ.get('PORT', 5000))

with open('environment.json') as f:
    env = json.load(f)

config = {
        'DATABASE_URI':env['DATABASE_URI'],
        'REDIS_URI':env['REDIS_URI'],
        'SESSION_KEY':env['SESSION_KEY']
         }

@manager.option('--no-rcon-check', dest='rcon_check', action='store_const',
        const=True, default=False)
@manager.option('--debug', dest='debug', action='store_const', const=True, default=False)
def run(debug, rcon_check):
    from random import randint
    from asciiart import print_image, print_title
    print_image()
    print_title()
    config_app(app, DEBUG=debug, RCON_CHECK_SERVER=(not rcon_check), **config)
    SocketIOServer(('', port), app, resource="socket.io",
            transports=['websocket', 'xhr-polling'], policy_server=False).serve_forever()

@manager.command
def init_db():
    config_app(app, **config)
    from lobbypy.utils import db
    db.create_all()

@manager.command
def drop_db():
    config_app(app, **config)
    from lobbypy.utils import db
    if prompt_bool(
            "Are you sure you want to clear the database"):
        db.drop_all()

@manager.option('steam_id', action='store')
def add_admin(steam_id):
    config_app(app, **config)
    from lobbypy.utils import db
    from lobbypy.models import Player
    player = Player.query.filter_by(steam_id = steam_id).first()
    if player:
        player.admin = True
    else:
        player = Player(steam_id)
        player.admin = True
    password = prompt_pass(
            "Enter password for the Administrator")
    if password == prompt_pass(
            "Re-enter password for the Administrator"):
        player.password = crypt(password)
        db.session.add(player)
        db.session.commit()
    else:
        print "Passwords do not match, re-run command"

if __name__ == '__main__':
    manager.run()
