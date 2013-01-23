from gevent import monkey; monkey.patch_all()
import json
import asciiart
from lobbypy import create_app, config_app

with open('/home/dotcloud/environment.json') as f:
    env = json.load(f)

config = {
        'DATABASE_URI':env['DOTCLOUD_DB_SQL_URL'].replace('pgsql', 'postgresql',
            1),
        'REDIS_URI':env['DOTCLOUD_DATA_REDIS_URL'],
        'SESSION_KEY':env['SESSION_KEY'],
        'STEAM_API_KEY':env['STEAM_API_KEY']
         }

asciiart.print_image()
asciiart.print_title()

app = create_app()
config_app(app, **config)
