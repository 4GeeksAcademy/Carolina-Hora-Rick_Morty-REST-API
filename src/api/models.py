from flask_sqlalchemy import SQLAlchemy
import enum

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    favorites = db.relationship("Favorites", backref= "user")


    def __repr__(self):
        return f'<{self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    status = db.Column(db.String(120), unique=False, nullable=True)
    species = db.Column(db.String(120), unique=False, nullable=True)
    gender = db.Column(db.String(120), unique=False, nullable=True)
    favorites = db.relationship("Favorites", backref= "characters")

    def __repr__(self):
        return f'<Characters {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "species": self.species,
            "gender": self.gender,
        }
    
class Locations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    type = db.Column(db.String(120), unique=False, nullable=True)
    dimension = db.Column(db.String(120), unique=False, nullable=True)
    favorites = db.relationship("Favorites", backref= "locations")

    def __repr__(self):
        return f'<Locations {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "dimension": self.dimension,
        }

class Episodes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    air_date = db.Column(db.String(120), unique=False, nullable=True)
    episode = db.Column(db.String(120), unique=False, nullable=True)
    favorites = db.relationship("Favorites", backref= "episodes")

    def __repr__(self):
        return f'<Episodes {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "air_date": self.air_date,
            "episode": self.episode,
        }
    
class Category (enum.Enum):
    characters = "characters"
    locations = "locations"
    episodes = "episodes"

class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.Enum(Category), server_default="characters")
    characters_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=True)
    locations_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=True)
    episodes_id = db.Column(db.Integer, db.ForeignKey('episodes.id'), nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "characters_id": self.characters_id,
            "locations_id": self.locations_id,
            "episodes_id": self.episodes_id,
        }