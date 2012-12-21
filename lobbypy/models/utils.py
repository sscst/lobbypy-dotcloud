def make_lobby_item_dict(l):
    return {
            'id': l.id,
            'name': l.name,
            'owner': make_player_dict(l.owner),
            'game_map': l.game_map,
            'player_count': l.player_count,
            'spectator_count': l.spectator_count,
            }

def make_lobby_dict(l):
    return {
            'id': l.id,
            'name': l.name,
            'owner': make_player_dict(l.owner),
            'game_map': l.game_map,
            'teams': [make_team_dict(i, t) for i,t in enumerate(l.teams)],
            'spectators': [make_player_dict(p) for p in l.spectators],
            }

def make_team_dict(i, t):
    return {
            'id': i,
            'name': t.name,
            'players': [make_lobby_player_dict(lp) for lp in t.players],
            }

def make_lobby_player_dict(lp):
    return {
            'class_id': lp.class_id,
            'ready': lp.ready,
            'player': make_player_dict(lp.player),
            }

def make_player_dict(p):
    return {
            'id': p.id,
            'steam_id': p.steam_id,
            'name': p.name
            }

