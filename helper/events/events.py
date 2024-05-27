from back_end.db import get_db
import sqlite3
import uuid
def add_event(event_name, event_status, event_date, user_id ):
    conn = get_db()
    cursor = conn.cursor()
    event_id = str(uuid.uuid4())
    try:
        cursor.execute('''
            INSERT INTO events (event_id, event_name, event_date, event_status, user_id) 
            VALUES (?,?, ?, ?,?)
        ''', (event_id, event_name, event_date, event_status, user_id))
        conn.commit()
    except sqlite3.IntegrityError as e:
        return False, str(e)
    finally:
        conn.close()
    return True, "event added successfully"
def get_current_events(user_id):
    conn = get_db()
    cursor = conn.cursor()
    
    query = '''
        SELECT 
        e.event_id, 
        strftime('%Y-%m-%d %H:%M:%S', e.event_date) AS event_date, 
        e.event_status, 
        e.event_name, 
        s.suggestion_id, 
        s.place, 
        s.category,
        COALESCE(uv.upvote_count, 0) AS upvote_count,
        COALESCE(dv.downvote_count, 0) AS downvote_count,
        CASE 
            WHEN uv_current.user_id IS NOT NULL THEN uv_current.vote_type
            ELSE NULL
        END AS user_vote_type,
        uv_current.vote_id 
    FROM events e
    LEFT JOIN suggestions s ON e.event_id = s.event_id
    LEFT JOIN (
        SELECT suggestion_id, COUNT(*) AS upvote_count
        FROM votes
        WHERE vote_type = 'upvote'
        GROUP BY suggestion_id
    ) uv ON s.suggestion_id = uv.suggestion_id
    LEFT JOIN (
        SELECT suggestion_id, COUNT(*) AS downvote_count
        FROM votes
        WHERE vote_type = 'downvote'
        GROUP BY suggestion_id
    ) dv ON s.suggestion_id = dv.suggestion_id
    LEFT JOIN (
        SELECT suggestion_id, vote_id, vote_type, user_id  
        FROM votes
        WHERE user_id = ?
    ) uv_current ON s.suggestion_id = uv_current.suggestion_id
    WHERE e.event_status = 'current'

    '''
    cursor.execute(query, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    
    # Transform the result into the desired format
    events_dict = {}
    for row in rows:
        event_id = row['event_id']
        if event_id not in events_dict:
            events_dict[event_id] = {
                'event_id': row['event_id'],
                'event_date': row['event_date'],
                'event_status': row['event_status'],
                'event_name': row['event_name'],
                'suggestions': []
            }
        
        suggestion = {
            'suggestion_id': row['suggestion_id'],
            'place': row['place'],
            'category': row['category'],
            'upvote_count': row['upvote_count'],
            'downvote_count': row['downvote_count'],
            'user_vote_type': row['user_vote_type'],
            'vote_id' : row['vote_id']
        }
        
        events_dict[event_id]['suggestions'].append(suggestion)
    
    return list(events_dict.values())

def get_freezed_events(user_id):
    conn = get_db()
    cursor = conn.cursor()

    query = '''
        SELECT 
            e.event_id, 
            strftime('%Y-%m-%d %H:%M:%S', e.event_date) AS event_date, 
            e.event_status, 
            e.event_name, 
            s.suggestion_id, 
            s.place, 
            s.category,
            COALESCE(ua.upvote_count, 0) AS upvote_count,
            COALESCE(da.downvote_count, 0) AS downvote_count,
            ua_current.availability_id,
            CASE 
                WHEN ua_current.user_id IS NOT NULL THEN ua_current.vote_type
                ELSE NULL
            END AS user_vote_type
        FROM events e
        LEFT JOIN suggestions s ON e.event_id = s.event_id AND s.is_chosen = 1
        LEFT JOIN (
            SELECT suggestion_id, COUNT(*) AS upvote_count
            FROM user_availability
            WHERE is_available = 1
            GROUP BY suggestion_id
        ) ua ON s.suggestion_id = ua.suggestion_id
        LEFT JOIN (
            SELECT suggestion_id, COUNT(*) AS downvote_count
            FROM user_availability
            WHERE is_available = 0
            GROUP BY suggestion_id
        ) da ON s.suggestion_id = da.suggestion_id
        LEFT JOIN (
            SELECT suggestion_id, user_id, is_available AS vote_type, availability_id
            FROM user_availability
            WHERE user_id = ?
        ) ua_current ON s.suggestion_id = ua_current.suggestion_id
        WHERE e.event_status = 'freezed';


    '''
    cursor.execute(query, (user_id,))
    rows = cursor.fetchall()
    conn.close()

    # Transform the result into the desired format
    events_dict = {}
    for row in rows:
        event_id = row['event_id']
        if event_id not in events_dict:
            events_dict[event_id] = {
                'event_id': row['event_id'],
                'event_date': row['event_date'],
                'event_status': row['event_status'],
                'event_name': row['event_name'],
                'suggestions': []
            }
        
        suggestion = {
            'suggestion_id': row['suggestion_id'],
            'place': row['place'],
            'category': row['category'],
            'upvote_count': row['upvote_count'],
            'downvote_count': row['downvote_count'],
            'user_vote_type': row['user_vote_type'],
            'availability_id': row['availability_id']
        }
        
        events_dict[event_id]['suggestions'].append(suggestion)
    
    return list(events_dict.values())

def get_finished_events():
    conn = get_db()
    cursor = conn.cursor()

    query = '''
        SELECT 
            e.event_id, 
            strftime('%Y-%m-%d %H:%M:%S', e.event_date) AS event_date, 
            e.event_status, 
            e.event_name, 
            s.suggestion_id, 
            s.place, 
            s.category,
            COALESCE(ua.upvote_count, 0) AS upvote_count,
            COALESCE(da.downvote_count, 0) AS downvote_count
        FROM events e
        LEFT JOIN suggestions s ON e.event_id = s.event_id AND s.is_chosen = 1
        LEFT JOIN (
            SELECT suggestion_id, COUNT(*) AS upvote_count
            FROM user_availability
            WHERE is_available = 1
            GROUP BY suggestion_id
        ) ua ON s.suggestion_id = ua.suggestion_id
        LEFT JOIN (
            SELECT suggestion_id, COUNT(*) AS downvote_count
            FROM user_availability
            WHERE is_available = 0
            GROUP BY suggestion_id
        ) da ON s.suggestion_id = da.suggestion_id
        WHERE e.event_status = 'finished';


    '''
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    # Transform the result into the desired format
    events_dict = {}
    for row in rows:
        event_id = row['event_id']
        if event_id not in events_dict:
            events_dict[event_id] = {
                'event_id': row['event_id'],
                'event_date': row['event_date'],
                'event_status': row['event_status'],
                'event_name': row['event_name'],
                'suggestions': []
            }
        
        suggestion = {
            'suggestion_id': row['suggestion_id'],
            'place': row['place'],
            'category': row['category'],
            'upvote_count': row['upvote_count'],
            'downvote_count': row['downvote_count'],
        }
        
        events_dict[event_id]['suggestions'].append(suggestion)
    
    return list(events_dict.values())
def update_event_status(event_id, new_status, suggestion_id):
    conn = get_db()
    cursor = conn.cursor()

    # Check current status of the event
    cursor.execute('SELECT event_status FROM events WHERE event_id = ?', (event_id,))
    event = cursor.fetchone()
    
    if not event:
        raise ValueError('Event not found')
    
    current_status = event['event_status']

    # Validate status transition
    if current_status == 'current' and new_status != 'freezed':
        raise ValueError('Invalid status transition from current to ' + new_status)
    elif current_status == 'freezed' and new_status != 'finished':
        raise ValueError('Invalid status transition from freezed to ' + new_status)
    elif current_status == 'finished':
        raise ValueError('Cannot change status of a finished event')

    # If transitioning to 'freezed', update the chosen suggestion
    if new_status == 'freezed':
        if not suggestion_id:
            raise ValueError('suggestion_id is required when changing status to freezed')

        # Update the chosen suggestion
        cursor.execute('UPDATE suggestions SET is_chosen = 1 WHERE suggestion_id = ?', (suggestion_id,))
        if cursor.rowcount == 0:
            raise ValueError('Suggestion not found or already chosen')
    
    # Update event status
    cursor.execute('UPDATE events SET event_status = ? WHERE event_id = ?', (new_status, event_id))
    conn.commit()
    conn.close()

    return 'Event status updated successfully'