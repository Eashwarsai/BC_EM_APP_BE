from  db import get_db
import sqlite3
import uuid
def add_suggestion(place, category, event_id, is_chosen=False):
    conn = get_db()
    cursor = conn.cursor()
    suggestion_id = str(uuid.uuid4())
    try:
        cursor.execute('''
            INSERT INTO suggestions (suggestion_id, place, category, event_id, is_chosen) 
            VALUES (?,?, ?, ?, ?)
        ''', (suggestion_id, place, category, event_id, is_chosen))
        conn.commit()
    except sqlite3.IntegrityError as e:
        return False, str(e)
    finally:
        conn.close()
    return True, "suggestion added successfully"

