from   ...db import get_db
import sqlite3
import uuid
from flask import session
def add_user(username, password_hash, email, is_admin=False):
    conn = get_db()
    cursor = conn.cursor()
    user_id = str(uuid.uuid4())
    # print(session)
    get_data = session.get('is_admin')
    print(get_data)
    # print(session.get('is_admin'))
    if session.get('is_admin'):
        try:
            cursor.execute('''
                INSERT INTO users (user_id, username, password_hash, email, is_admin) 
                VALUES (?,?, ?, ?, ?)
            ''', (user_id, username, password_hash, email, is_admin))
            conn.commit()
        except sqlite3.IntegrityError as e:
            return False, str(e)
        finally:
            conn.close()
        return True, "User added successfully"
    else:
        return False, "You are not authorized to add user"

def get_user_by_email(email):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM users WHERE email = ?
    ''', (email,))
    user = cursor.fetchone()
    
    conn.close()
    return user
