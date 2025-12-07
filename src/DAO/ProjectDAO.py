import sqlite3
from pathlib import Path
from typing import List, Optional

from Models.Project import Project


DB_NAME = "a.db"


def _get_db_path() -> Path:
    # repository root is parent of this DAO folder
    return Path(__file__).resolve().parents[1] / DB_NAME


def _get_conn():
    p = _get_db_path()
    conn = sqlite3.connect(str(p))
    conn.row_factory = sqlite3.Row
    return conn


class ProjectDAO:
    def __init__(self):
        pass

    def create(self, title: str) -> int:
        sql = "INSERT INTO Project (title) VALUES (?)"
        with _get_conn() as conn:
            cur = conn.execute(sql, (title,))
            return cur.lastrowid

    def get(self, project_id: int) -> Optional[Project]:
        sql = "SELECT project_id, title FROM Project WHERE project_id = ?"
        with _get_conn() as conn:
            cur = conn.execute(sql, (project_id,))
            row = cur.fetchone()
            if row:
                return Project.from_row(dict(row))
        return None

    def list_all(self) -> List[Project]:
        sql = "SELECT project_id, title FROM Project ORDER BY title"
        with _get_conn() as conn:
            cur = conn.execute(sql)
            return [Project.from_row(dict(r)) for r in cur.fetchall()]

    def update(self, project: Project) -> bool:
        sql = "UPDATE Project SET title = ? WHERE project_id = ?"
        with _get_conn() as conn:
            cur = conn.execute(sql, (project.title, project.project_id))
            return cur.rowcount > 0

    def delete(self, project_id: int) -> bool:
        sql = "DELETE FROM Project WHERE project_id = ?"
        with _get_conn() as conn:
            cur = conn.execute(sql, (project_id,))
            return cur.rowcount > 0
class ProjectDAO:
    def __init__(self):
        pass

    # Add project-related data access methods here