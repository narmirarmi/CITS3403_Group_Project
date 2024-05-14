from faker import Faker
import random
from datetime import datetime, timedelta
import sys
import os
from werkzeug.security import generate_password_hash

# Get the current directory of this script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory (root directory) to the Python path
project_dir = os.path.dirname(current_dir)
sys.path.append(project_dir)
from database.models import *
from app import app


# Don't change the seed please
SEED = 4321
fake = Faker()
Faker.seed(SEED)
random.seed(SEED)

# populate the database with random users
def create_users(n):
    users = []
    emails = {}
    for _ in range(n):
        username = fake.user_name()
        email = fake.email()
        password = hash_password(fake.password(length=12))
        profile_picture = fake.image_url()
        user = User(username=username, email=email, password=password, profile_picture=profile_picture)
        users.append(user)
    db.session.add_all(users)
    db.session.commit()
    return users

# populate the database with random images
def create_images(users):
    images = []
    for user in users:
        for _ in range(random.randint(0,
                                      3)):  # Each user will have 1-3 images (maybe we should make it 0-x but for now 1-3 is fine
            image_path = fake.image_url()
            upload_date = datetime.utcnow() - timedelta(days=random.randint(0, 10))
            image = Image(user_id=user.id, image_path=image_path, upload_date=upload_date)
            images.append(image)
    db.session.add_all(images)
    db.session.commit()
    return images

# populate the datbase with random votes
def create_votes(users, images):
    votes = []
    for image in images:
        sampled_users = random.sample(users,
                                      random.randint(1, len(users)))  # Each image gets 1 to all users voting on it
        for user in sampled_users:
            type = random.choice(['like', 'dislike'])
            vote = Vote(image_id=image.id, user_id=user.id, type=type)
            votes.append(vote)
    db.session.add_all(votes)
    db.session.commit()

# populate the database with random comments
def create_comments(users, images):
    comments = []
    for image in images:
        sampled_users = random.sample(users, random.randint(1, len(users)))  # Each image gets 1 to all users commenting
        for user in sampled_users:
            text = fake.sentence()
            comment_date = image.upload_date + timedelta(days=random.randint(0, 10))
            comment = Comment(image_id=image.id, user_id=user.id, text=text, comment_date=comment_date)
            comments.append(comment)
    db.session.add_all(comments)
    db.session.commit()

# populate the database with random follows
def create_follows(users):
    follows = []
    for user in users:
        other_users = [u for u in users if u != user]
        sampled_users = random.sample(other_users, random.randint(1,
                                                                  len(other_users) // 2))  # Each user follows half of the other users
        for followee in sampled_users:
            follow = Follow(follower_id=user.id, followee_id=followee.id)
            follows.append(follow)
    db.session.add_all(follows)
    db.session.commit()

# create dummy data using above functions
def add_dummy_data():
    # Generate Users
    users = create_users(10)  # Creating 10 dummy users
    # Generate Images
    images = create_images(users)
    # Generate Votes
    create_votes(users, images)
    # Generate Comments
    create_comments(users, images)
    # Generate Follows
    create_follows(users)

def hash_password(password):
    bytes = password.encode('utf-8')
    password_hash = generate_password_hash(password, method="pbkdf2:md5")
    return password_hash

def reset_db():
    with app.app_context():
        print("Resetting database...")
        db.drop_all()

# main function call
if __name__ == '__main__':
    with app.app_context():
        db.init_app(app)
        reset_db()
        db.create_all()  # Ensure that all tables are created
        add_dummy_data()
        print("Dummy data has been added to the database.")