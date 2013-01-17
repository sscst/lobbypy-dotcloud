from lobbypy.utils import db
spectator_table = db.Table('spectator', db.metadata,
        db.Column('lobby_id', db.Integer, db.ForeignKey('lobby.id'), primary_key=True),
        db.Column('player_id', db.Integer, db.ForeignKey('player.id'),
                primary_key=True),
        )

class Lobby(db.Model):
    __tablename__ = 'lobby'
    id = db.Column(db.Integer, primary_key=True)
    discriminator = db.Column('type', db.String)
    name = db.Column(db.String, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False,
            unique=True)
    teams = db.relationship('Team', backref='lobby',
            cascade='save-update,merge,delete')
    spectators = db.relationship('Player', secondary=spectator_table)
    lock = db.Column(db.Boolean, nullable=False, default=False)
    server_address = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    game_map = db.Column(db.String, nullable=False)
    __mapper_args__ = {'polymorphic_on': discriminator}

    def __init__(self, name, owner, server_address, game_map, password,
            teams=None):
        self.name = name
        self.owner = owner
        self.server_address = server_address
        self.game_map = game_map
        self.password = password
        if teams is None:
            self.teams = self._defaultTeams()

    def __contains__(self, player):
        return player in self.spectators or any([player in t for t in
            self.teams])

    def __len__(self):
        return self.player_count + self.spectator_count

    def _defaultTeams(self):
        return [Team('Red'), Team('Blu')]

    @property
    def player_count(self):
        return sum([len(t) for t in self.teams])

    @property
    def spectator_count(self):
        return len(self.spectators)

    def join(self, player):
        # TODO: do we complain here, or act like a set and ignore double joins?
        assert player not in self
        self.spectators.append(player)

    def leave(self, player):
        if player in self.spectators:
            self.spectators.remove(player)
        else:
            for team in self.teams:
                if player in team:
                    team.leave(player)

    def _pop(self, player):
        if player in self.spectators:
            self.spectators.remove(player)
            return player
        else:
            for team in self.teams:
                if player in team:
                    return team._pop(player)

    def set_team(self, player, team_id):
        our_player = self._pop(player)
        if team_id is None:
            self.spectators.append(player)
        else:
            team = self.teams[team_id]
            if isinstance(our_player, LobbyPlayer):
                team.append(our_player)
            else:
                team.join(player)

    def set_class(self, player, class_id):
        [t.set_class(player, class_id) for t in self.teams if player in t]

    def is_ready_player(self, player):
        for team in self.teams:
            if player in team:
                lp = team.get_lobby_player(player)
                return lp.ready

    def toggle_ready(self, player):
        [t.toggle_ready(player) for t in self.teams if player in t]

class HighlanderLobby(Lobby):
    __mapper_args__ = {'polymorphic_identity': 'highlander'}

    def _defaultTeams(self):
        return [HighlanderTeam('Red'), HighlanderTeam('Blu')]

class SixesLobby(Lobby):
    __mapper_args__ = {'polymorphic_identity': 'sixes'}

    def _defaultTeams(self):
        return [SixesTeam('Red'), SixesTeam('Blu')]

class Team(db.Model):
    __tablename__ = 'team'
    id = db.Column(db.Integer, primary_key=True)
    discriminator = db.Column('type', db.String)
    name = db.Column(db.String, nullable=False)
    lobby_id = db.Column(db.Integer, db.ForeignKey('lobby.id'), nullable=False)
    players = db.relationship('LobbyPlayer', backref='team',
            cascade='save-update,merge,delete,delete-orphan')
    __mapper_args__ = {'polymorphic_on': discriminator}

    def __init__(self, name):
        self.name = name

    def __len__(self):
        return len(self.players)

    def __contains__(self, player):
        return any([lp.player == player for lp in self.players])

    def can_join(self):
        return True

    def can_set_class(self, class_id):
        return class_id is None or class_id >= 0 and class_id < 9

    def class_count(self, class_id):
        return len([lp for lp in self.players
            if lp.class_id == class_id])

    def get_lobby_player(self, player):
        lps = [lp for lp in self.players if lp.player == player]
        return lps.pop()

    def append(self, lobby_player):
        assert lobby_player.player not in self
        self.players.append(lobby_player)

    def remove(self, lobby_player):
        self.players.remove(lobby_player)

    def _pop(self, player):
        lp = self.get_lobby_player(player)
        self.players.remove(lp)
        return lp

    def join(self, player):
        assert player not in self
        assert self.can_join()
        self.append(LobbyPlayer(player))

    def leave(self, player):
        lp = self.get_lobby_player(player)
        self.remove(lp)

    def set_class(self, player, class_id):
        assert self.can_set_class(class_id)
        lp = self.get_lobby_player(player)
        lp.class_id = class_id

    def toggle_ready(self, player):
        lp = self.get_lobby_player(player)
        lp.ready = not lp.ready

class HighlanderTeam(Team):
    __mapper_args__ = {'polymorphic_identity': 'highlander'}

    def can_join(self):
        return len(self) < 9

    def can_set_class(self, class_id):
        return (super(HighlanderTeam, self).can_set_class(class_id)
                and (class_id is None or class_id not in
                    [lp.class_id for lp in self.players]))

class SixesTeam(Team):
    __mapper_args__ = {'polymorphic_identity': 'sixes'}

    def can_join(self):
        return len(self) < 6

    def can_set_class(self, class_id):
        return (super(SixesTeam, self).can_set_class(class_id)
                and self._can_set_class(class_id))

    def _can_set_class(self, class_id):
        if class_id == 0 or class_id == 1:
            return self.class_count(class_id) < 2
        elif class_id == 3 or class_id == 6:
            return self.class_count(class_id) < 1
        elif class_id is None:
            return True
        return False

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
