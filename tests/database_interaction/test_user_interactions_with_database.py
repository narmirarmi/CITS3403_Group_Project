import unittest
from flask import Flask
from database.models import db, User, Image, Vote, Comment, Follow
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class SocialMediaAppTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        cls.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        cls.app.config['UPLOAD_FOLDER'] = '/path/to/upload'
        db.init_app(cls.app)
        with cls.app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.drop_all()

    def setUp(self):
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.connection = db.engine.connect()
        self.transaction = self.connection.begin()
        db.session.bind = self.connection

    def tearDown(self):
        db.session.remove()
        self.transaction.rollback()
        self.connection.close()
        self.app_context.pop()

    def test_follow_and_unfollow(self):
        user1 = User(username='user1', email='user1@example.com', password='pass')
        user2 = User(username='user2', email='user2@example.com', password='pass')
        db.session.add_all([user1, user2])
        db.session.commit()

        # Simulate following and unfollowing
        follow = Follow(follower_id=user1.id, followee_id=user2.id)
        db.session.add(follow)
        db.session.commit()
        self.assertEqual(len(user1.followers), 1)

        db.session.delete(follow)
        db.session.commit()
        self.assertEqual(len(user1.followers), 0)

    def test_like_dislike(self):
        user = User(username='testuser', email='test@example.com', password='pass')
        image = Image(user_id=user.id, image_path='path/to/image.jpg', post_title='Test Post',
                      post_description='Description')
        db.session.add_all([user, image])
        db.session.commit()

        vote = Vote(image_id=image.id, user_id=user.id, type='like')
        db.session.add(vote)
        db.session.commit()
        self.assertEqual(Vote.query.filter_by(type='like').count(), 1)

        vote.type = 'dislike'
        db.session.commit()
        self.assertEqual(Vote.query.filter_by(type='dislike').count(), 1)

    def test_image_upload(self):
        user = User(username='charlie', email='charlie@example.com', password='pass')
        db.session.add(user)
        db.session.commit()

        image = Image(user_id=user.id, image_path='tests/test_data/burger.jpg', post_title='Test Image',
                      post_description='A test image.')
        db.session.add(image)
        db.session.commit()

        stored_image = Image.query.first()
        self.assertEqual(stored_image.user_id, user.id)
        self.assertEqual(stored_image.image_path, 'tests/test_data/burger.jpg')

    def test_comment_on_image(self):
        user = User(username='alice', email='alice@example.com', password=generate_password_hash('pass'))
        db.session.add(user)
        db.session.commit()

        image = Image(user_id=user.id, image_path='path/to/image.jpg', post_title='Test Post',
                      post_description='Description')
        db.session.add(image)
        db.session.commit()

        comment = Comment(image_id=image.id, user_id=user.id, text='Nice pic!')
        db.session.add(comment)
        db.session.commit()
        self.assertEqual(len(image.comments), 1)
        self.assertEqual(image.comments[0].text, 'Nice pic!')


if __name__ == '__main__':
    unittest.main()
