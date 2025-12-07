import sqlite3
from pathlib import Path
from typing import List, Optional

from Models.TodoItem import TodoItem


DB_NAME = "a.db"


def _get_db_path() -> Path:
    return Path(__file__).resolve().parents[1] / DB_NAME


def _get_conn():
    p = _get_db_path()
    conn = sqlite3.connect(str(p))
    conn.row_factory = sqlite3.Row
    return conn


class TodoItemDAO:
    def __init__(self):
        pass

    def create(self, item: TodoItem) -> int:
        sql = (
            "INSERT INTO Todo_Item (title, description, priority, completed, project_id, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?)"
        )
        with _get_conn() as conn:
            cur = conn.execute(sql, item.to_tuple_for_insert())
            return cur.lastrowid

    def get(self, todo_id: int) -> Optional[TodoItem]:
        sql = "SELECT todo_id, title, description, priority, completed, project_id, created_at FROM Todo_Item WHERE todo_id = ?"
        with _get_conn() as conn:
            cur = conn.execute(sql, (todo_id,))
            row = cur.fetchone()
            if row:
                return TodoItem.from_row(dict(row))
        return None

    def list_all(self, project_id: Optional[int] = None) -> List[TodoItem]:
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
        sql = (
            "UPDATE Todo_Item SET title = ?, description = ?, priority = ?, completed = ?, project_id = ?, created_at = ? WHERE todo_id = ?"
        )
        with _get_conn() as conn:
            cur = conn.execute(sql, item.to_tuple_for_update())
            return cur.rowcount > 0

    def delete(self, todo_id: int) -> bool:
        sql = "DELETE FROM Todo_Item WHERE todo_id = ?"
        with _get_conn() as conn:
            cur = conn.execute(sql, (todo_id,))
            return cur.rowcount > 0
class TodoItemDAO:
    def __init__(self):
        pass

    # Add todo item-related data access methods here
