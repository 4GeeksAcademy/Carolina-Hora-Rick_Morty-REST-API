"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Characters, Locations, Episodes, Favorites
from api.utils import generate_sitemap, APIException

api = Blueprint("api", __name__)

# To Fix: The DELETE user and DELETE Favorites are not working properly!


@api.route("/hello", methods=["POST", "GET"])
def handle_hello():
    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200


@api.route("/user", methods=["GET"])
def get_all_users():
    users = User.query.all()
    serialized_users = [user.serialize() for user in users]
    # 'serialize()' method is used to convert the users object into a JSON format that can be easily sent over the API.
    # if we don't use the 'serialize()' method it will give an error saying that "the object type Users is not serializable, meaning that the API can not read it."
    # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    # print(users)
    # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    return jsonify(serialized_users), 200


@api.route("/user/<int:user_id>", methods=["GET"])
def get_one_user_by_id(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "No user found with this id"}), 400
    return jsonify(user.serialize()), 200


@api.route("/user/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    body = request.json
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "No user found with this id"}), 400

    user.email = body["email"]
    user.password = body["password"]
    db.session.commit()
    return jsonify("User updated"), 200


@api.route("/user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "No user found with this id"}), 400

    db.session.delete(user)
    db.session.commit()
    return jsonify("User deleted"), 200


# This DELETE only works on users which have not selected any favorites


@api.route("/characters", methods=["GET"])
def get_all_characters():
    characters = Characters.query.all()
    serialized_characters = [character.serialize() for character in characters]
    # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    # print("Hello Characters:", characters)
    # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    return jsonify(serialized_characters), 200


@api.route("/character/<int:characters_id>", methods=["GET"])
def get_one_character_by_id(characters_id):
    character = Characters.query.get(characters_id)
    if not character:
        return jsonify({"error": "No character found with this id"}), 400
    return jsonify(character.serialize()), 200


@api.route("/character", methods=["POST"])
def create_character():
    body = request.json
    new_character = Characters(
        name=body["name"],
        status=body["status"],
        species=body["species"],
        gender=body["gender"],
    )
    db.session.add(new_character)
    db.session.commit()
    return jsonify("Character created"), 200


@api.route("/character/<int:character_id>", methods=["PUT"])
def update_character(character_id):
    character = Characters.query.get(character_id)
    if not character:
        return jsonify({"error": "No character found with this id"}), 400

    body = request.json

    character.name = body.get("name", character.name)
    character.status = body.get("status", character.status)
    character.species = body.get("species", character.species)
    character.gender = body.get("gender", character.gender)

    db.session.commit()
    return jsonify("Character updated"), 200


@api.route("/character/<int:character_id>", methods=["DELETE"])
def delete_character(character_id):
    character = Characters.query.get(character_id)
    if not character:
        return jsonify({"error": "No character found with this id"}), 400

    db.session.delete(character)
    db.session.commit()
    return jsonify("character deleted"), 200


@api.route("/locations", methods=["GET"])
def get_all_locations():
    locations = Locations.query.all()
    serialized_locations = [location.serialize() for location in locations]
    # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    # print("Hello Locations", locations, serialized_locations)
    # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    return jsonify(serialized_locations), 200


@api.route("/location", methods=["POST"])
def create_location():
    body = request.json
    new_location = Locations(
        name=body["name"],
        type=body["type"],
        dimension=body["dimension"],
    )
    db.session.add(new_location)
    db.session.commit()
    return jsonify("location created"), 200


@api.route("/location/<int:location_id>", methods=["PUT"])
def update_location(location_id):
    location = Locations.query.get(location_id)
    if not location:
        return jsonify({"error": "No location found with this id"}), 400

    body = request.json

    location.name = body.get("name", location.name)
    location.type = body.get("type", location.type)
    location.dimension = body.get("dimension", location.dimension)

    db.session.commit()
    return jsonify("location updated"), 200


@api.route("/location/<int:location_id>", methods=["DELETE"])
def delete_location(location_id):
    location = Locations.query.get(location_id)
    if not location:
        return jsonify({"error": "No location found with this id"}), 400

    db.session.delete(location)
    db.session.commit()
    return jsonify("location deleted"), 200


@api.route("/location/<int:locations_id>", methods=["GET"])
def get_one_location_by_id(locations_id):
    location = Locations.query.get(locations_id)
    if not location:
        return jsonify({"error": "No location found with this id"}), 400
    return jsonify(location.serialize()), 200


@api.route("/episodes", methods=["GET"])
def get_all_episodes():
    episodes = Episodes.query.all()
    serialized_episodes = [episode.serialize() for episode in episodes]
    # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    # print("Hello Episodes", episodes)
    # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

    return jsonify(serialized_episodes), 200


@api.route("/episode/<int:episodes_id>", methods=["GET"])
def get_one_episode_by_id(episodes_id):
    episode = Episodes.query.get(episodes_id)
    if not episode:
        return jsonify({"error": "No episode found with this id"}), 400
    return jsonify(episode.serialize()), 200


@api.route("/episode", methods=["POST"])
def create_episode():
    body = request.json
    new_episode = Episodes(
        name=body["name"],
        air_date=body["air_date"],
        episode=body["episode"],
    )
    db.session.add(new_episode)
    db.session.commit()
    return jsonify("episode created"), 200


@api.route("/episode/<int:episode_id>", methods=["PUT"])
def update_episode(episode_id):
    episode = Episodes.query.get(episode_id)
    if not episode:
        return jsonify({"error": "No episode found with this id"}), 400

    body = request.json

    episode.name = body.get("name", episode.name)
    episode.air_date = body.get("air_date", episode.air_date)
    episode.episode = body.get("episode", episode.episode)

    db.session.commit()
    return jsonify("episode updated"), 200


@api.route("/episode/<int:episode_id>", methods=["DELETE"])
def delete_episode(episode_id):
    episode = Episodes.query.get(episode_id)
    if not episode:
        return jsonify({"error": "No episode found with this id"}), 400

    db.session.delete(episode)
    db.session.commit()
    return jsonify("episode deleted"), 200


@api.route("/user/favorites", methods=["GET"])
def get_all_favorites():
    favorites = Favorites.query.all()
    serialized_favorites = [favorite.serialize() for favorite in favorites]
    # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    # print("Hello Favorites", favorites)
    # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

    return jsonify(serialized_favorites), 200


@api.route("/user/favorite/<int:favorites_id>", methods=["GET"])
def get_one_favorite_by_id(favorites_id):
    favorite = Favorites.query.get(favorites_id)
    if not favorite:
        return jsonify({"error": "No favorite found with this id"}), 400
    return jsonify(favorite.serialize()), 200


@api.route("/user/favorites/<category>/<int:id>", methods=["POST"])
def select_favorite_by_category(category, id):
    user_id = 1
    if category == "characters":
        favorite = Favorites(user_id=user_id, category="characters", characters_id=id)
    elif category == "locations":
        favorite = Favorites(user_id=user_id, category="locations", locations_id=id)
    elif category == "episodes":
        favorite = Favorites(user_id=user_id, category="episodes", episodes_id=id)

    db.session.add(favorite)
    db.session.commit()
    return jsonify("Favorite by " + category + " created"), 200


@api.route("/user/favorites/<category>/<int:id>", methods=["DELETE"])
def delete_favorite_by_category(category, id):
    user_id = 1
    if category == "characters":
        favorite = Favorites(user_id=user_id, category="characters", characters_id=id)
    elif category == "locations":
        favorite = Favorites(user_id=user_id, category="locations", locations_id=id)
    elif category == "episodes":
        favorite = Favorites(user_id=user_id, category="episodes", episodes_id=id)

    db.session.delete(favorite)
    db.session.commit()
    return jsonify("Favorite by " + category + " deleted"), 200


# @api.route("/user/favorites/character/<int:characters_id>", methods=["POST"])
# def select_favorite_character(characters_id):
#     user_id = 1
#     favorite = Favorites(
#         user_id=user_id, category="characters", characters_id=characters_id
#     )

#     db.session.add(favorite)
#     db.session.commit()
#     return jsonify("Favorite character created"), 200


# @api.route("/user/favorites/location/<int:locations_id>", methods=["POST"])
# def select_favorite_location(locations_id):
#     user_id = 1
#     favorite = Favorites(
#         user_id=user_id, category="locations", locations_id=locations_id
#     )

#     db.session.add(favorite)
#     db.session.commit()
#     return jsonify("Favorite location created"), 200


# @api.route("/user/favorites/episode/<int:episodes_id>", methods=["POST"])
# def select_favorite_episode(episodes_id):
#     user_id = 1
#     favorite = Favorites(user_id=user_id, category="episodes", episodes_id=episodes_id)

#     db.session.add(favorite)
#     db.session.commit()
#     return jsonify("Favorite episode created"), 200
