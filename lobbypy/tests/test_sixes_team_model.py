from flask.ext.testing import TestCase
from lobbypy import create_app, config_app
from lobbypy.utils import db

class SixesTeamModelTest(TestCase):
    def create_app(self):
        app = create_app()
        config_app(app, SQLALCHEMY_DATABASE_URI='sqlite://', TESTING=True)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def _makeOne(self, name='Red'):
        from lobbypy.models import SixesTeam
        return SixesTeam(name)

    def test_can_join(self):
        instance = self._makeOne()
        self.assertTrue(instance.can_join())

    def test_not_can_join(self):
        instance = self._makeOne()
        from lobbypy.models import Player
        for i in range(6):
            p = Player('%d' % i)
            p.id = i
            instance.join(p)
        self.assertTrue(not instance.can_join())

    def test_can_set_class(self):
        instance = self._makeOne()
        for i in [0, 1, 3, 6]:
            self.assertTrue(instance.can_set_class(i))
        self.assertTrue(instance.can_set_class(None))
        from lobbypy.models import Player
        instance.join(Player('0'))
        instance.players[0].class_id = 0
        self.assertTrue(instance.can_set_class(0))
        instance.players[0].class_id = 1
        self.assertTrue(instance.can_set_class(1))

    def test_not_can_set_class(self):
        instance = self._makeOne()
        self.assertTrue(not instance.can_set_class(-1))
        self.assertTrue(not instance.can_set_class(2))
        from lobbypy.models import Player
        p1 = Player('0')
        p2 = Player('0')
        p1.id = 1
        p2.id = 2
        instance.join(p1)
        instance.join(p2)
        instance.players[0].class_id = 0
        instance.players[1].class_id = 0
        self.assertTrue(not instance.can_set_class(0))
        instance.players[0].class_id = 6
        self.assertTrue(not instance.can_set_class(6))

