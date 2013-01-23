from lobbypy.utils import db
from lobbypy.lib import get_player_summary_for_steam_id

class Player(db.Model):
    __tablename__ = 'player'
    id = db.Column(db.Integer, primary_key=True)
    steam_id = db.Column(db.String(40), unique=True)
    lobby = db.relationship('Lobby', uselist=False, backref='owner')
    # only used for admins/mods
    password = db.Column(db.String(48), nullable=True)
    admin = db.Column(db.Boolean, default=False, nullable=False)
    auth_attempts = db.Column(db.Integer, default=0, nullable=False)

    def __init__(self, steam_id):
        self.steam_id = steam_id

    def __eq__(self, other):
        return isinstance(other, Player) and self.id == other.id

    def __ne__(self, other):
        return not isinstance(other, Player) and self.id != other.id

    @staticmethod
    def get_or_create(steam_id):
        rv = Player.query.filter_by(steam_id=steam_id).first()
        if rv is None:
            rv = Player(steam_id)
            db.session.add(rv)
        return rv

    def _get_player_summary(self):
        return get_player_summary_for_steam_id(self.steam_id)

    @property
    def name(self):
        try:
            return self._get_player_summary()['personaname']
        except LookupError:
            return 'Unknown'
