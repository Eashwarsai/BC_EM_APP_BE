import uuid
from ...db import get_db

def update_or_create_vote_db(vote_id, suggestion_id, user_id, vote_type):
    conn = get_db()
    cursor = conn.cursor()

    if vote_id:
        # Update the vote type
        cursor.execute('''
            UPDATE votes
            SET vote_type = ?
            WHERE vote_id = ?
        ''', (vote_type, vote_id))
        message = 'Vote updated successfully'
    else:
        # Create a new vote
        new_vote_id = str(uuid.uuid4())
        cursor.execute('''
            INSERT INTO votes (vote_id, suggestion_id, user_id, vote_type)
            VALUES (?, ?, ?, ?)
        ''', (new_vote_id, suggestion_id, user_id, vote_type))
        vote_id = new_vote_id
        message = 'Vote created successfully'

    conn.commit()
    conn.close()

    return message, vote_id
