import uuid
from ...db import get_db

def update_or_create_user_availability_db(availability_id , suggestion_id, user_id, is_available):
    conn = get_db()
    cursor = conn.cursor()

    if availability_id:
        # Update the vote type
        cursor.execute('''
            UPDATE user_availability
            SET is_available = ?
            WHERE availability_id = ?
        ''', (is_available, availability_id))
        message = 'availability vote updated successfully'
    else:
        # Create a new vote
        new_availability_id = str(uuid.uuid4())
        cursor.execute('''
            INSERT INTO user_availability (availability_id, suggestion_id, user_id, is_available)
            VALUES (?, ?, ?, ?)
        ''', (new_availability_id, suggestion_id, user_id, is_available))
        availability_id = new_availability_id
        message = 'availability vote created successfully'

    conn.commit()
    conn.close()

    return message, availability_id
