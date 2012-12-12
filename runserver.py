import os
from flask.ext.script import Manager, prompt_bool

from lobbypy import create_app
app = create_app()

manager = Manager(app)
# Bind to PORT if defined, otherwise default to 5000.
port = int(os.environ.get('PORT', 5000))

@manager.command
def run():
    app.run(host='0.0.0.0', port=port)

@manager.command
def init_db():
    from lobbypy import db
    db.create_all()

@manager.command
def drop_db():
    from lobbypy import db
    if prompt_bool(
            "Are you sure you want to clear the database"):
        db.drop_all()

if __name__ == '__main__':
    manager.run()
