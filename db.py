import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    """
    Retrieves a database connection from the Flask application context.

    If the 'db' key is not present in the Flask application context, a new database connection is established using the 
    value of the 'DATABASE' configuration key in the Flask application. The connection is configured to detect SQL types.

    Returns:
        sqlite3.Connection: The database connection object.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    """
    Closes the database connection.

    Parameters:
        e (Exception, optional): An exception object. Defaults to None.

    Returns:
        None
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """
    Initializes the database by executing the SQL statements in the 'schema.sql' file.

    This function connects to the database using the `get_db()` function and executes the SQL statements
    contained in the 'schema.sql' file. The 'schema.sql' file should be located in the same directory as
    the 'db.py' file.

    Parameters:
        None

    Returns:
        None
    """
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """
    Initializes the database by executing the SQL statements in the 'schema.sql' file.

    This function is a Click command that initializes the database by executing the SQL statements
    contained in the 'schema.sql' file. The 'schema.sql' file should be located in the same directory
    as the 'db.py' file.

    Parameters:
        None

    Returns:
        None
    """
    init_db()
    click.echo('Initialized the database!')

def init_app(app):
    """
    Initializes the Flask application by setting up the database connection and adding the `init-db` command to the CLI.

    Args:
        app (Flask): The Flask application instance.

    Returns:
        None
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
