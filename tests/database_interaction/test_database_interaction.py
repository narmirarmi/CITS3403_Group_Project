import unittest
from database.models import *

import unittest
from database.models import db, User, Image
from flask import Flask

class TestDatabaseInteractions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        cls.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(cls.app)
        with cls.app.app_context():
            db.create_all()

    def tearDownClass(self, cls):
        with cls.app.app_context():
            db.drop_all()

    def setUp(self):
        # Push an application context to make sure we can interact with the db
        self.app_context = self.app.app_context()
        self.app_context.push()
        # Use the db.session directly provided by Flask-SQLAlchemy
        self.connection = db.engine.connect()
        self.transaction = self.connection.begin()
        db.session.bind = self.connection

    def tearDown(self):
        db.session.remove()
        self.transaction.rollback()
        self.connection.close()
        self.app_context.pop()

    def test_user_constraints(self):
        user = User(username='john', email='john@example.com', password='pass123')
        db.session.add(user)
        db.session.commit()

        user2 = User(username='john', email='john2@example.com', password='pass1234')
        db.session.add(user2)
        with self.assertRaises(Exception):
            db.session.commit()

        user3 = User(email='john3@example.com', password='pass123')
        db.session.add(user3)
        with self.assertRaises(Exception):
            db.session.commit()

    def test_user_relationships(self):
        user = User(username='alice', email='alice@example.com', password='pass123')
        db.session.add(user)
        db.session.commit()

        image = Image(user_id=user.id, image_path='tests/test_data/burger.jpg', post_title='Test Image',
                      post_description='A test image.')
        db.session.add(image)
        db.session.commit()

        self.assertEqual(user.images[0].id, image.id)

    def test_user_authentication(self):
        user = User(username='bob', email='bob@example.com', password='pass123')
        db.session.add(user)
        db.session.commit()

        self.assertTrue(user.is_authenticated())
        self.assertTrue(user.is_active())
        self.assertFalse(user.is_anonymous())
        self.assertEqual(user.get_id(), str(user.id))

    def test_image_upload(self):
        user = User(username='charlie', email='charlie@example.com', password='pass123')
        db.session.add(user)
        db.session.commit()

        image = Image(user_id=user.id, image_path='tests/test_data/burger.jpg', post_title='Test Image',
                      post_description='A test image.')
        db.session.add(image)
        db.session.commit()

        stored_image = Image.query.first()
        self.assertEqual(stored_image.user_id, user.id)
        self.assertEqual(stored_image.image_path, 'tests/test_data/burger.jpg')


if __name__ == '__main__':
    unittest.main()
