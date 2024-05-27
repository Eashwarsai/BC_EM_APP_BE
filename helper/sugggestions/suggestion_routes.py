from flask import Blueprint,request, jsonify
from .suggestions import add_suggestion
suggestion_routes = Blueprint('suggestion_routes', __name__)

@suggestion_routes.route('/suggestions', methods=['POST'])
def suggestions_endpoint():
    if request.method=='POST':
        data = request.get_json()
        place = data.get('place')
        category = data.get('category')
        event_id = data.get('event_id')
        is_chosen = data.get('is_chosen', False)
        success, message = add_suggestion(place, category, event_id, is_chosen)
        if success:
            return jsonify({'message': message}), 201
        else:
            return jsonify({'error': message}), 400