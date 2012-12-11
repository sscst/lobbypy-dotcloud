from .db import db

spectator_table = db.Table('spectator', db.metadata,
        db.Column('lobby_id', db.Integer, db.ForeignKey('lobby.id'), primary_key=True),
        db.Column('player_id', db.Integer, db.ForeignKey('player.id'),
                primary_key=True),
        )

class Lobby(db.Model):
    __tablename__ = 'lobby'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False,
            unique=True)
    teams = db.relationship('Team', backref='lobby',
            cascade='save-update,merge,delete')
    spectators = db.relationship('Player', secondary=spectator_table)
    lock = db.Column(db.Boolean, nullable=False, default=False)
    server = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    game_map = db.Column(db.String, nullable=False)

    def __init__(self, name, owner, server, game_map, password):
        self.name = name
        self.owner = owner
        self.server = server
        self.game_map = game_map
        self.password = password

class Team(db.Model):
    __tablename__ = 'team'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    lobby_id = db.Column(db.Integer, db.ForeignKey('lobby.id'), nullable=False)
    players = db.relationship('LobbyPlayer', backref='team',
            cascade='save-update,merge,delete,delete-orphan')

    def __init__(self, name):
        self.name = name

class LobbyPlayer(db.Model):
    __tablename__ = 'lobby_player'
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), primary_key=True)
    player = db.relationship('Player', uselist=False)
    player_class = db.Column(db.Integer)
    ready = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, player, player_class=None):
        self.player = player
        self.player_class = player_class
