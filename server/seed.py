#!/usr/bin/env python3

import os
import sys
from random import randint, choice as rc
from faker import Faker
from app import app, db
from models import Game, Review, User

# Add the project directory to the Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_dir)

fake = Faker()

# Initialize the Flask app and the database
with app.app_context():
    # Clear existing data
    Review.query.delete()
    User.query.delete()
    Game.query.delete()

    # Create users
    users = [User(name=fake.name()) for _ in range(100)]
    db.session.add_all(users)

    # Create games
    genres = ["Platformer", "Shooter", "Fighting", "Stealth", "Survival", "Rhythm", "Survival Horror", "Metroidvania", "Text-Based", "Visual Novel", "Tile-Matching", "Puzzle", "Action RPG", "MMORPG", "Tactical RPG", "JRPG", "Life Simulator", "Vehicle Simulator", "Tower Defense", "Turn-Based Strategy", "Racing", "Sports", "Party", "Trivia", "Sandbox"]
    platforms = ["NES", "SNES", "Nintendo 64", "GameCube", "Wii", "Wii U", "Nintendo Switch", "GameBoy", "GameBoy Advance", "Nintendo DS", "Nintendo 3DS", "XBox", "XBox 360", "XBox One", "XBox Series X/S", "PlayStation", "PlayStation 2", "PlayStation 3", "PlayStation 4", "PlayStation 5", "PSP", "PS Vita", "Genesis", "DreamCast", "PC"]

    games = [Game(
        title=fake.sentence(),
        genre=rc(genres),
        platform=rc(platforms),
        price=randint(5, 60),
    ) for _ in range(100)]
    db.session.add_all(games)

    # Create reviews
    reviews = []
    for user in users:
        for _ in range(randint(1, 10)):
            review = Review(
                score=randint(0, 10),
                comment=fake.sentence(),
                user=user,
                game=rc(games)
            )
            reviews.append(review)

    db.session.add_all(reviews)

    # Assign reviews to games
    for game in games:
        review = rc(reviews)
        game.reviews.append(review)
        reviews.remove(review)

    # Commit changes to the database
    db.session.commit()
