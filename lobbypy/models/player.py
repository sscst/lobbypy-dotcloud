from lobbypy.models.db import db

class Player(db.Model):
    __tablename__ = 'player'
    id = db.Column(db.Integer, primary_key=True)
    steam_id = db.Column(db.String(40), unique=True)
    #lobby = relationship('Lobby', uselist=False, backref='owner')

    def __init__(self, steam_id):
        self.steam_id = steam_id

    @staticmethod
    def get_or_create(steam_id):
        rv = Player.query.filter_by(steam_id=steam_id).first()
        if rv is None:
            rv = Player(steam_id)
            db.session.add(rv)
        return rv
