from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Episode(db.Model):
    __tablename__ = 'episodes'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    number = db.Column(db.Integer, nullable=False)

    # Relationship: has many appearances
    appearances = db.relationship('Appearance', backref='episode', lazy=True, cascade='all, delete-orphan')

    def to_dict(self, include_appearances=False):
        episode_dict = {
            'id': self.id,
            'date': self.date,
            'number': self.number
        }
        if include_appearances:
            episode_dict['appearances'] = [appearance.to_dict(include_guest=True) for appearance in self.appearances]
        return episode_dict

class Guest(db.Model):
    __tablename__ = 'guests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    occupation = db.Column(db.String, nullable=True)

    # Relationship: has many appearances
    appearances = db.relationship('Appearance', backref='guest', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'occupation': self.occupation
        }

class Appearance(db.Model):
    __tablename__ = 'appearances'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'), nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validate_rating()

    def validate_rating(self):
        if self.rating is not None and (self.rating < 1 or self.rating > 5):
            raise ValueError("Rating must be between 1 and 5")

    def to_dict(self, include_guest=False, include_episode=False):
        appearance_dict = {
            'id': self.id,
            'rating': self.rating,
            'guest_id': self.guest_id,
            'episode_id': self.episode_id
        }
        if include_guest:
            appearance_dict['guest'] = self.guest.to_dict()
        if include_episode:
            appearance_dict['episode'] = self.episode.to_dict()
        return appearance_dict
