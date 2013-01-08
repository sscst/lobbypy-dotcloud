from json import dumps
from flask import g, session
from flask.ext.testing import TestCase
from lobbypy import create_app, config_app
from lobbypy.utils import db
from lobbypy.models import Player, Lobby, Team

class RestTest(TestCase):
    def create_app(self):
        app = create_app()
        config_app(app, SQLALCHEMY_DATABASE_URI='sqlite://', TESTING=True)
        return app

    def setUp(self):
        db.create_all()
        a = Player('')
        a.admin = True
        db.session.add(a)
        db.session.commit()
        self.admin = a
        with self.client.session_transaction() as sess:
            sess['user_id'] = a.id

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_player(self):
        resp = self.client.post('/admin/rest/players', data=dict(steam_id='0'))
        p = Player.query.filter_by(steam_id = '0').first()
        self.assertStatus(resp, 201)
        self.assertTrue(p)
        self.assertEqual(p.steam_id, '0')

    def test_update_player(self):
        p = Player('0')
        db.session.add(p)
        db.session.commit()
        resp = self.client.put('/admin/rest/players/%d' % p.id,
                data=dict(steam_id='1'))
        self.assertStatus(resp, 200)
        p = db.session.merge(p)
        self.assertEqual(p.steam_id, '1')

    def test_delete_player(self):
        p = Player('0')
        db.session.add(p)
        db.session.commit()
        resp = self.client.delete('/admin/rest/players/%d' % p.id)
        self.assertStatus(resp, 200)
        players = Player.query.filter_by(steam_id = '0').all()
        self.assertEqual(len(players), 0)

    def test_create_lobby(self):
        resp = self.client.post('/admin/rest/lobbies', data=dict(owner_id =
            self.admin.id, name = 'Lobby', server_address = 'x.x.x.x',
            rcon_password = 'xxxx', game_map = 'xxxxx', password = 'xxxx'))
        self.assertStatus(resp, 201)
        l = Lobby.query.first()
        self.assertEqual(l.name, 'Lobby')

    def test_update_lobby(self):
        l = Lobby('Lobby', self.admin, 'test', 'test', 'test', 'test')
        db.session.add(l)
        db.session.commit()
        resp = self.client.put('/admin/rest/lobbies/%d' % l.id, data=dict(name = 'Test'))
        self.assertStatus(resp, 200)
        l = db.session.merge(l)
        self.assertEqual(l.name, 'Test')

    def test_delete_lobby(self):
        l = Lobby('Lobby', self.admin, 'test', 'test', 'test', 'test')
        db.session.add(l)
        db.session.commit()
        resp = self.client.delete('/admin/rest/lobbies/%d' % l.id)
        lobbies = Lobby.query.all()
        self.assertStatus(resp, 200)
        self.assertEqual(len(lobbies), 0)

    def test_append_team(self):
        l = Lobby('Lobby', self.admin, 'test', 'test', 'test', 'test')
        db.session.add(l)
        db.session.commit()
        resp = self.client.post('/admin/rest/lobbies/%d/teams' % l.id,
                data=dict(name='Red'))
        self.assertStatus(resp, 201)
        l = db.session.merge(l)
        self.assertEqual(len(l.teams), 1)
        self.assertEqual(l.teams[0].name, 'Red')

    def test_update_team(self):
        l = Lobby('Lobby', self.admin, 'test', 'test', 'test', 'test')
        t = Team('Red')
        l.teams.append(t)
        db.session.add(l)
        db.session.commit()
        resp = self.client.put('/admin/rest/lobbies/%d/teams/0' % l.id,
                data=dict(name='Blu'))
        self.assertStatus(resp, 200)
        l = db.session.merge(l)
        self.assertEqual(l.teams[0].name, 'Blu')

    def test_delete_team(self):
        l = Lobby('Lobby', self.admin, 'test', 'test', 'test', 'test')
        t = Team('Red')
        l.teams.append(t)
        db.session.add(l)
        db.session.commit()
        resp = self.client.delete('/admin/rest/lobbies/%d/teams/0' % l.id)
        self.assertStatus(resp, 200)
        l = db.session.merge(l)
        self.assertEqual(len(l.teams), 0)

    def test_append_spectator(self):
        l = Lobby('Lobby', self.admin, 'test', 'test', 'test', 'test')
        p = Player('0')
        db.session.add(p)
        db.session.add(l)
        db.session.commit()
        resp = self.client.post('/admin/rest/lobbies/%d/spectators' % l.id,
                data=dict(player_id = p.id))
        self.assertStatus(resp, 200)
        l = db.session.merge(l)
        self.assertEqual(len(l.spectators), 1)

    def test_remove_spectator(self):
        l = Lobby('Lobby', self.admin, 'test', 'test', 'test', 'test')
        p = Player('0')
        l.spectators.append(p)
        db.session.add(p)
        db.session.add(l)
        db.session.commit()
        resp = self.client.delete('/admin/rest/lobbies/%d/spectators/%d' % (
            l.id, p.id))
        self.assertStatus(resp, 200)
        l = db.session.merge(l)
        self.assertEqual(len(l.spectators), 0)

    def test_append_lobby_player(self):
        l = Lobby('Lobby', self.admin, 'test', 'test', 'test', 'test')
        t = Team('Red')
        p = Player('0')
        l.teams.append(t)
        db.session.add(p)
        db.session.add(l)
        db.session.commit()
        resp = self.client.post('/admin/rest/lobbies/%d/teams/0/players' %
            l.id, data=dict(player_id = p.id))
        self.assertStatus(resp, 201)
        l = db.session.merge(l)
        self.assertEqual(len(l.teams[0].players), 1)

    def test_update_lobby_player(self):
        l = Lobby('Lobby', self.admin, 'test', 'test', 'test', 'test')
        t = Team('Red')
        p = Player('0')
        t.append_player(p)
        l.teams.append(t)
        db.session.add(p)
        db.session.add(l)
        db.session.commit()
        resp = self.client.put('/admin/rest/lobbies/%d/teams/0/players/%d' %
            (l.id, p.id), data=dict(class_id = 0))
        self.assertStatus(resp, 200)
        l = db.session.merge(l)
        self.assertEqual(len(l.teams[0].players), 1)
        self.assertEqual(l.teams[0].players[0].class_id, 0)

    def test_delete_lobby_player(self):
        l = Lobby('Lobby', self.admin, 'test', 'test', 'test', 'test')
        t = Team('Red')
        p = Player('0')
        t.append_player(p)
        l.teams.append(t)
        db.session.add(p)
        db.session.add(l)
        db.session.commit()
        resp = self.client.delete('/admin/rest/lobbies/%d/teams/0/players/%d' %
            (l.id, p.id))
        self.assertStatus(resp, 200)
        l = db.session.merge(l)
        self.assertEqual(len(l.teams[0].players), 0)
