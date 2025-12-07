import sqlite3
from pathlib import Path


DB_PATH = "Databases/TodoList.db"

def _get_db_path() -> Path:
    """Return the file system path to the SQLite database file.

    Returns:
        Path: absolute path to the database file in the repository root.
    """
    # repository root is parent of this DAO folder
    return Path(__file__).resolve().parents[1] / DB_PATH


def _get_conn():
    """Create and return a sqlite3.Connection to the configured DB.

    Returns:
        sqlite3.Connection: connection object with row_factory set to sqlite3.Row
    """
    p = _get_db_path()
    print("Database path:", str(p))
    conn = sqlite3.connect(str(p))
    conn.row_factory = sqlite3.Row
    return conn