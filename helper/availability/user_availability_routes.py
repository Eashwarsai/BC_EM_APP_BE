from flask import Blueprint, request, jsonify
from ...db import get_db
from .user_availability import update_or_create_user_availability_db

user_availability_routes = Blueprint('user_availability_routes', __name__)

@user_availability_routes.route('/availability', methods=['PATCH'])
def update_or_create_availability_vote():
    data = request.get_json()
    availability_id = data.get('availability_id',None)
    suggestion_id = data.get('suggestion_id')
    user_id = data.get('user_id')
    is_available = data.get('is_available')

    if not suggestion_id or not user_id :
        return jsonify({'error': 'suggestion_id, user_id, and is_available parameters are required'}), 400

    try:
        message, new_availability_id = update_or_create_user_availability_db(availability_id, suggestion_id, user_id, is_available)
        return jsonify({'message': message, 'availability_id': new_availability_id}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'An error occurred: ' + str(e)}), 500
