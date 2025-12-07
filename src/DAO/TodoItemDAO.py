import sqlite3
from pathlib import Path
from typing import List, Optional

from Models.TodoItem import TodoItem


DB_NAME = "TodoList.db"


def _get_db_path() -> Path:
    """Return the path to the SQLite database file.

    Returns:
        Path: database file path in repository root.
    """
    return Path(__file__).resolve().parents[1] / DB_NAME


def _get_conn():
    """Create and return a sqlite3 connection.

    Returns:
        sqlite3.Connection: connection object (row_factory=sqlite3.Row)
    """
    p = _get_db_path()
    conn = sqlite3.connect(str(p))
    conn.row_factory = sqlite3.Row
    return conn


class TodoItemDAO:
    """Data access object for `Todo_Item` records."""

    def __init__(self):
        """Initialize the DAO instance.

        No parameters. Database path is determined from module-level settings.
        """
        pass

    def create(self, item: TodoItem) -> Optional[int]:
        """Insert a new todo item into the database.

        Parameters:
            item (TodoItem): domain object containing todo fields. `todo_id` is ignored.

        Returns:
            int: the new row id (todo_id).
        """
        sql = (
            "INSERT INTO Todo_Item (title, description, priority, completed, project_id, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?)"
        )
        with _get_conn() as conn:
            cur = conn.execute(sql, item.to_tuple_for_insert())
            return cur.lastrowid

    def get(self, todo_id: int) -> Optional[TodoItem]:
        """Fetch a todo item by its id.

        Parameters:
            todo_id (int): primary key of the todo item.

        Returns:
            Optional[TodoItem]: `TodoItem` if found, otherwise `None`.
        """
        sql = "SELECT todo_id, title, description, priority, completed, project_id, created_at FROM Todo_Item WHERE todo_id = ?"
        with _get_conn() as conn:
            cur = conn.execute(sql, (todo_id,))
            row = cur.fetchone()
            if row:
                return TodoItem.from_row(dict(row))
        return None

    def list_all(self, project_id: Optional[int] = None) -> List[TodoItem]:
        """List todo items, optionally filtered by project.

        Parameters:
            project_id (Optional[int]): if provided, only todos for this project are returned.

        Returns:
            List[TodoItem]: list of `TodoItem` instances (may be empty).
        """
        if project_id is None:
            sql = "SELECT todo_id, title, description, priority, completed, project_id, created_at FROM Todo_Item ORDER BY created_at DESC"
            params = ()
        else:
            sql = "SELECT todo_id, title, description, priority, completed, project_id, created_at FROM Todo_Item WHERE project_id = ? ORDER BY created_at DESC"
            params = (project_id,)
        with _get_conn() as conn:
            cur = conn.execute(sql, params)
            return [TodoItem.from_row(dict(r)) for r in cur.fetchall()]

    def update(self, item: TodoItem) -> bool:
        """Update an existing todo item.

        Parameters:
            item (TodoItem): `TodoItem` with `todo_id` set and updated fields.

        Returns:
            bool: True if a row was updated, False otherwise.
        """
        sql = (
            "UPDATE Todo_Item SET title = ?, description = ?, priority = ?, completed = ?, project_id = ?, created_at = ? WHERE todo_id = ?"
        )
        with _get_conn() as conn:
            cur = conn.execute(sql, item.to_tuple_for_update())
            return cur.rowcount > 0

    def delete(self, todo_id: int) -> bool:
        """Delete a todo item by id.

        Parameters:
            todo_id (int): id of the todo to delete.

        Returns:
            bool: True if a row was deleted, False otherwise.
        """
        sql = "DELETE FROM Todo_Item WHERE todo_id = ?"
        with _get_conn() as conn:
            cur = conn.execute(sql, (todo_id,))
            return cur.rowcount > 0
