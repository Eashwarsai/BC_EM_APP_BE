from flask import Blueprint,request, jsonify
from .events import get_current_events,add_event,get_freezed_events,get_finished_events,update_event_status
event_routes = Blueprint('event_routes', __name__)


@event_routes.route('/events', methods=['GET','POST','PATCH'])
def get_event_by_status_endpoint():
    if request.method=='POST':
        data = request.get_json()
        success, message = add_event(data['event_name'], data['event_status'], data['event_date'],data['user_id'] )
        if success:
            return jsonify({'message': message}), 201
        else:
            return jsonify({'error': message}), 400
    if request.method=='GET':
        status = request.args.get('event_status')
        user_id=request.args.get('user_id',None)
        if not status:
            return jsonify({'error': 'event_status parameter is required'}), 400
        
        if status == 'current':
            events = get_current_events(user_id)
        elif status == 'freezed':
            events = get_freezed_events(user_id)
        else:
            events = get_finished_events()
        if events:
            return jsonify(events)
        else:
            return jsonify([]), 200
    if request.method=='PATCH':
        event_id = request.args.get('event_id')
        new_status = request.args.get('to')
        suggestion_id = request.args.get('suggestion_id',None)
        if not event_id or not new_status:
            return jsonify({'error': 'event_id and to parameters are required'}), 400
        
        if new_status not in ['freezed', 'finished']:
            return jsonify({'error': 'Invalid status. It must be "freezed" or "finished"'}), 400


        try:
            message = update_event_status(event_id, new_status, suggestion_id)
            return jsonify({'message': message}), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': 'An error occurred: ' + str(e)}), 500