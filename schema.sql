-- DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS suggestions;
DROP TABLE IF EXISTS votes;
DROP TABLE IF EXISTS user_availability;

-- CREATE TABLE users (
--     user_id TEXT PRIMARY KEY,
--     username TEXT NOT NULL,
--     password_hash TEXT NOT NULL,
--     email TEXT UNIQUE NOT NULL,
--     is_admin BOOLEAN NOT NULL DEFAULT 0
-- );

CREATE TABLE events (
    event_id TEXT PRIMARY KEY,
    event_date TIMESTAMP NOT NULL,
    event_status TEXT NOT NULL,
    event_name TEXT NOT NULL,
    user_id TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    CHECK (event_status IN ('current', 'freezed', 'finished'))
);

CREATE TABLE suggestions (
    suggestion_id TEXT PRIMARY KEY,
    place TEXT NOT NULL,
    category TEXT NOT NULL,
    is_chosen BOOLEAN NOT NULL DEFAULT 0,
    event_id TEXT NOT NULL,
    FOREIGN KEY (event_id) REFERENCES events(event_id),
    CHECK (category IN ('BoardGames', 'Sports', 'Food'))
);

CREATE TABLE votes (
    vote_id TEXT PRIMARY KEY,
    suggestion_id TEXT  NOT NULL,
    user_id TEXT NOT NULL,
    vote_type TEXT NOT NULL,
    UNIQUE (suggestion_id, user_id),
    FOREIGN KEY (suggestion_id) REFERENCES suggestions(suggestion_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    CHECK (vote_type IN ('upvote', 'downvote'))
);

CREATE TABLE user_availability (
    availability_id TEXT PRIMARY KEY,
    suggestion_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    is_available BOOLEAN NOT NULL ,
    UNIQUE (suggestion_id, user_id),
    FOREIGN KEY (suggestion_id) REFERENCES suggestions(suggestion_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
