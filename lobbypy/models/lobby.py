from lobbypy import db
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

    @property
    def player_count(self):
        return sum([len(t) for t in self.teams])

    @property
    def spectator_count(self):
        return len(self.spectators)

    def join(self, player):
        self.spectators.append(player)

    def pop_player(self, player):
        if player in self.spectators:
            self.spectators.remove(player)
            return player
        else:
            for team in self.teams:
                if team.has_player(player):
                    return team.pop_player(player)

    def leave(self, player):
        if player in self.spectators:
            self.spectators.remove(player)
        else:
            for team in self.teams:
                if team.has_player(player):
                    team.remove_player(player)

    def set_team(self, player, team_id):
        our_player = self.pop_player(player)
        if team_id is None:
            self.spectators.append(player)
        else:
            team = self.teams[team_id]
            if isinstance(our_player, LobbyPlayer):
                team.append(our_player)
            else:
                team.append_player(player)

    def set_class(self, player, class_id):
        for team in self.teams:
            if team.has_player(player):
                team.set_class(player, class_id)

    def toggle_ready(self, player):
        for team in self.teams:
            if team.has_player(player):
                team.toggle_ready(player)

class Team(db.Model):
    __tablename__ = 'team'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    lobby_id = db.Column(db.Integer, db.ForeignKey('lobby.id'), nullable=False)
    players = db.relationship('LobbyPlayer', backref='team',
            cascade='save-update,merge,delete,delete-orphan')

    def __init__(self, name):
        self.name = name

    def __len__(self):
        return len(self.players)

    def has_player(self, player):
        return any([lp.player.id == player.id for lp in self.players])

    def get_lobby_player(self, player):
        lps = [lp for lp in self.players if lp.player.id == player.id]
        return lps.pop()

    def append(self, lobby_player):
        self.players.append(lobby_player)

    def pop_player(self, player):
        lp = self.get_lobby_player(player)
        self.players.remove(lp)
        return lp

    def append_player(self, player):
        self.players.append(LobbyPlayer(player))

    def remove_player(self, player):
        lp = self.get_lobby_player(player)
        self.players.remove(lp)

    def set_class(self, player, class_id):
        lp = self.get_lobby_player(player)
        lp.class_id = class_id

    def toggle_ready(self, player):
        lp = self.get_lobby_player(player)
        lp.ready = not lp.ready

class LobbyPlayer(db.Model):
    __tablename__ = 'lobby_player'
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), primary_key=True)
    player = db.relationship('Player', uselist=False)
    class_id = db.Column(db.Integer)
    ready = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, player, player_class=None):
        self.player = player
        self.player_class = player_class
