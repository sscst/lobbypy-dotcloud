import unittest
from mock import Mock, patch

class PlayerModelTest(unittest.TestCase):
    @patch('lobbypy.models.player.get_player_summary_for_steam_id')
    def test_get_player_summary(self, mock_method):
        from lobbypy.models import Player
        instance = Player('0')
        mock_method.return_value = {}
        rv = instance._get_player_summary()
        mock_method.assert_called_once_with('0')
        self.assertEqual(rv, {})

    @patch('lobbypy.models.player.get_player_summary_for_steam_id')
    def test_name(self, mock_method):
        from lobbypy.models import Player
        instance = Player('0')
        mock_method.return_value = {'personaname': 'test'}
        rv = instance.name
        self.assertEqual(rv, 'test')
