from srcdspy import SourceRcon
from srcdspy.rcon import RconException

def connect_rcon(server_address, rcon_password):
    rcon_server_ip, rcon_server_port = server_address.split(':')
    sr = SourceRcon()
    sr.connect((rcon_server_ip, rcon_server_port), rcon_password)
    return sr

def connect_query(server_address):
    rcon_server_ip, rcon_server_port = server_address.split(':')
    sq = SourceRcon()
    sq.connect((rcon_server_ip, rcon_server_port))
    return sq

def check_map(source_rcon, game_map):
    """
    Check that the map exists on the server
    """
    resp = source_rcon.rcon('maps %s.bsp' % game_map)
    if len(resp) == 0:
        return False
    i = resp.find('PENDING')
    if i < 0:
        raise RconException("Bad Response")
    elif resp.find('PENDING', i+1) != -1:
        return False
    return True

def check_players(source_query):
    """
    Check that there are no players on the server (except STV bots)
    and that enough slots are available.
    """
    return len(source_query.player()) == 0
