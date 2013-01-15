from flask.ext.testing import TestCase
from lobbypy import create_app, config_app
from lobbypy.utils import db

class HighlanderTeamModelTest(TestCase):
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
        from lobbypy.models import HighlanderTeam
        return HighlanderTeam(name)

    def test_can_join(self):
        instance = self._makeOne()
        self.assertTrue(instance.can_join())

    def test_not_can_join(self):
        instance = self._makeOne()
        from lobbypy.models import Player
        for i in range(9):
            p = Player('%d' % i)
            p.id = i
            instance.join(p)
        self.assertTrue(not instance.can_join())

    def test_can_set_class(self):
        instance = self._makeOne()
        for i in range(9):
            self.assertTrue(instance.can_set_class(i))
        self.assertTrue(instance.can_set_class(None))

    def test_not_can_set_class(self):
        instance = self._makeOne()
        from lobbypy.models import Player
        for i in range(9):
            p = Player('%d' % i)
            p.id = i
            instance.join(p)
            instance.players[-1].class_id = i
        for i in range(9):
            self.assertTrue(not instance.can_set_class(i))
