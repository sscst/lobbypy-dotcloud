from srcdspy import SourceRcon

def connect(server_info):
    rcon_pass, server_info = rcon_info.split('@')
    rcon_server_ip, rcon_server_port = server_info.split(':')
    s = SourceRcon()
    s.connect((rcon_server_ip, rcon_server_port), rcon_pass)
    return s

def check_map(server, game_map):
    """
    Check that the map exists on the server
    """
    return False

def check_players(server):
    """
    Check that there are no players on the server (except STV bots)
    and that enough slots are available.
    """
    return False
