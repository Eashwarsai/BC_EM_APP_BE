from flask import Blueprint,request, jsonify, session
from .users import get_user_by_email, add_user

user_routes = Blueprint('user_routes', __name__)
@user_routes.route('/users', methods=['POST','GET'])
def user_endpoint():
    if request.method=='POST':
        data = request.get_json()
        username = data.get('username')
        password_hash = data.get('password_hash')
        email = data.get('email')
        is_admin = data.get('is_admin', False)

        success, message = add_user(username, password_hash, email, is_admin)
        if success:
            return jsonify({'message': message}), 201
        else:
            return jsonify({'error': message}), 400
    if request.method=='GET':
        email = request.args.get('email')
        if not email:
            return jsonify({'error': 'Email parameter is required'}), 400
        
        user = get_user_by_email(email)
        if user:
            session.permanent = True 
            session['is_admin']= user['is_admin']
            print(session)
            return jsonify({
                'user_id': user['user_id'],
                'username': user['username'],
                'email': user['email'],
                'password_hash': user['password_hash'],
                'is_admin': user['is_admin']
            }), 200
        else:
            return jsonify({'error': 'User not found'}), 404

@user_routes.route('/logout')
def logout():
    session.pop("is_admin",None)
    print(session)
    return jsonify({'message':'logged out successfully'}), 200