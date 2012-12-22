def make_lobby_item_dict(l):
    """lobby_item schema:
       {
           "name": "loboby_item",
           "properties": {
               "id" {
                   "description": "Id of the Lobby",
                   "type": "number",
                   "required": true
               },
               "name": {
                   "description": "Name of the Lobby",
                   "type": "string",
                   "required": true
               },
               "owner": {
                   "description": "Owner of the Lobby",
                   "type": PLAYER_SCHEMA,
                   "required": true
               },
               "game_map": {
                   "description": "Map for the Lobby",
                   "type": "string",
                   "required": true
               },
               "player_count": {
                   "description": "Count of players in the Lobby",
                   "type": "number",
                   "required": true
               },
               "spectator_count": {
                   "description": "Count of the spectators in the Lobby",
                   "type": "number"
                   "required": true
               }
           }
       }
    """
    return {
            'id': l.id,
            'name': l.name,
            'owner': make_player_dict(l.owner),
            'game_map': l.game_map,
            'player_count': l.player_count,
            'spectator_count': l.spectator_count,
            }

def make_lobby_dict(l):
    """lobby_item schema:
       {
           "name": "loboby_item",
           "properties": {
               "id": {
                   "description": "Id of the Lobby",
                   "type": "number",
                   "required": true
               },
               "name": {
                   "description": "Name of the Lobby",
                   "type": "string",
                   "required": true
               },
               "owner": {
                   "description": "Owner of the Lobby",
                   "type": PLAYER_SCHEMA,
                   "required": true
               },
               "game_map": {
                   "description": "Map for the Lobby",
                   "type": "string",
                   "required": true
               },
               "teams": {
                   "description": "Teams in the Lobby",
                   "type": "array",
                   "items": {
                       "type": TEAM_SCHEMA
                   },
                   "required": true
               },
               "spectators": {
                   "description": "Spectators in the Lobby",
                   "type": "array",
                   "items": {
                       "type": PLAYER_SCHEMA
                   },
                   "required": true
               }
           }
       }
    """
    return {
            'id': l.id,
            'name': l.name,
            'owner': make_player_dict(l.owner),
            'game_map': l.game_map,
            'teams': [make_team_dict(i, t) for i,t in enumerate(l.teams)],
            'spectators': [make_player_dict(p) for p in l.spectators],
            }

def make_team_dict(i, t):
    """team schema:
       {
           "name": "team",
           "properties": {
               "id": {
                   "description": "Id of the Team",
                   "type": "number",
                   "required": true
               },
               "name": {
                   "description": "Name of the Team",
                   "type": "string",
                   "required": true
               },
               "players": {
                   "description": "List of Players in the Team",
                   "type": "array",
                   "items": {
                       "type": LOBBY_PLAYER_SCHEMA
                   },
                   "required": true
               }
           }
       }
    """
    return {
            'id': i,
            'name': t.name,
            'players': [make_lobby_player_dict(lp) for lp in t.players],
            }

def make_lobby_player_dict(lp):
    """lobby_player schema:
        {
            "name": "lobby_player",
            "properties": {
                "class_id": {
                    "description": "Class for the Lobby Player",
                    "type": "string",
                    "required": true
                },
                "ready": {
                    "description": "Ready state for the Lobby Player",
                    "type": "boolean",
                    "required": true
                },
                "player": {
                    "description": "Player for this Lobby Player",
                    "type": PLAYER_SCHEMA,
                    "required": true
                }
            }
        }
    """
    return {
            'class_id': lp.class_id,
            'ready': lp.ready,
            'player': make_player_dict(lp.player),
            }

def make_player_dict(p):
    """player schema:
        {
            "name": "player",
            "properties": {
                "id": {
                    "description": "Id of the Player",
                    "type": "number",
                    "required": true
                },
                "steam_id": {
                    "description": "Steam ID for the Player",
                    "type": "string",
                    "required": true
                },
                "name": {
                    "description": "Name of the Player pulled from Steam",
                    "type": "string",
                    "required": true
                }
            }
        }
    """
    return {
            'id': p.id,
            'steam_id': p.steam_id,
            'name': p.name
            }

