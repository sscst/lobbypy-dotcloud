import json, urllib2
from flask import current_app
from lobbypy.utils import cache
def _get_api_key():
    return current_app.config['STEAM_API_KEY']

def _get_link_base():
    return 'http://api.steampowered.com/ISteamUser/'

def _get_player_summaries_link_base():
    return (_get_link_base() +
            'GetPlayerSummaries/v0002/?key=%s&steamids=' %
            _get_api_key())

def _get_player_friends_link_base():
    return (_get_link_base() +
            'GetFriendList/v0001/?key=%s&steamid=' %
            _get_api_key())

@cache.memoize(15*60)
def get_player_summary_for_steam_id(steam_id):
    link = '%s%s' % (_get_player_summaries_link_base(), steam_id)
    players = json.load(urllib2.urlopen(link))['response']['players']
    if len(players) != 1:
        raise LookupError('Error getting player summary from Steam API')
    return players[0]

@cache.memoize(60*60)
def get_player_friends_for_steam_id(steam_id):
    return json.load(urllib2.urlopen('%s%s' %
        (_get_player_friends_link_base(), steamid)))
