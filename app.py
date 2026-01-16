from flask import Flask, jsonify, request, abort
from app_package.models import db, Episode, Guest, Appearance

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lateshow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create tables on app startup
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return jsonify({
        'message': 'Late Show Management API',
        'endpoints': {
            'GET /episodes': 'Get all episodes',
            'GET /episodes/<id>': 'Get episode with appearances',
            'GET /guests': 'Get all guests',
            'POST /appearances': 'Create new appearance'
        }
    })

@app.route('/episodes', methods=['GET'])
def get_episodes():
    episodes = Episode.query.all()
    return jsonify([episode.to_dict() for episode in episodes])

@app.route('/episodes/<int:id>', methods=['GET'])
def get_episode(id):
    episode = Episode.query.get(id)
    if episode is None:
        abort(404, description="Episode not found")
    return jsonify(episode.to_dict(include_appearances=True))

@app.route('/guests', methods=['GET'])
def get_guests():
    guests = Guest.query.all()
    return jsonify([guest.to_dict() for guest in guests])

@app.route('/appearances', methods=['POST'])
def create_appearance():
    data = request.get_json()

    # Validate required fields
    if not data or 'rating' not in data or 'episode_id' not in data or 'guest_id' not in data:
        abort(400, description="Missing required fields: rating, episode_id, guest_id")

    rating = data['rating']
    episode_id = data['episode_id']
    guest_id = data['guest_id']

    # Validate rating
    if not isinstance(rating, int) or rating < 1 or rating > 5:
        abort(400, description="Rating must be an integer between 1 and 5")

    # Validate episode exists
    episode = Episode.query.get(episode_id)
    if episode is None:
        abort(400, description="Episode not found")

    # Validate guest exists
    guest = Guest.query.get(guest_id)
    if guest is None:
        abort(400, description="Guest not found")

    try:
        appearance = Appearance(rating=rating, episode_id=episode_id, guest_id=guest_id)
        db.session.add(appearance)
        db.session.commit()
        return jsonify(appearance.to_dict(include_guest=True, include_episode=True)), 201
    except ValueError as e:
        abort(400, description=str(e))

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': error.description}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': error.description}), 400

if __name__ == '__main__':
    app.run(port=5555, debug=True)
