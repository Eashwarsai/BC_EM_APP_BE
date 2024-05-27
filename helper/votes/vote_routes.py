from flask import Blueprint, request, jsonify
from ...db import get_db
from .votes import update_or_create_vote_db

vote_routes = Blueprint('vote_routes', __name__)

@vote_routes.route('/votes', methods=['PATCH'])
def update_or_create_vote():
    data = request.get_json()

    vote_id = data.get('vote_id', None)
    suggestion_id = data.get('suggestion_id')
    user_id = data.get('user_id')
    vote_type = data.get('vote_type')

    if not suggestion_id or not user_id or not vote_type:
        return jsonify({'error': 'suggestion_id, user_id, and vote_type parameters are required'}), 400

    if vote_type not in ['upvote', 'downvote']:
        return jsonify({'error': 'Invalid vote_type value. It must be "upvote" or "downvote"'}), 400

    try:
        message, new_vote_id = update_or_create_vote_db(vote_id, suggestion_id, user_id, vote_type)
        return jsonify({'message': message, 'vote_id': new_vote_id}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'An error occurred: ' + str(e)}), 500
