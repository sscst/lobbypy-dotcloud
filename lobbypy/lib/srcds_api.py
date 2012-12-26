from srcdspy import SRCDS

def connect(server_info):
    rcon_pass, server_info = rcon_info.split('@')
    rcon_server_ip, rcon_server_port = server_info.split(':')
    s = SRCDS()
    s.connect((rcon_server_ip, rcon_server_port), rcon_pass)
    return s

def check_map(server, game_map):
    return False

def check_players(server):
    return False
