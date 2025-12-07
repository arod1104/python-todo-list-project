import sqlite3
from pathlib import Path
from typing import List, Optional

from Models.Project import Project


import sqlite3
from pathlib import Path
from typing import List, Optional

from Models.Project import Project


DB_NAME = "TodoList.db"


def _get_db_path() -> Path:
    """Return the file system path to the SQLite database file.

    Returns:
        Path: absolute path to the database file in the repository root.
    """
    # repository root is parent of this DAO folder
    return Path(__file__).resolve().parents[1] / DB_NAME


def _get_conn():
    """Create and return a sqlite3.Connection to the configured DB.

    Returns:
        sqlite3.Connection: connection object with row_factory set to sqlite3.Row
    """
    p = _get_db_path()
    conn = sqlite3.connect(str(p))
    conn.row_factory = sqlite3.Row
    return conn


class ProjectDAO:
    """Data access object for `Project` records.

    All methods operate directly against the SQLite database file.
    """

    def __init__(self):
        """Initialize the DAO instance.

        No parameters. The DAO reads database path from module-level settings.
        """
        pass

    def addProject(self, title: str) -> Optional[Project]:
        """Insert a new Project row.

        Parameters:
            title (str): Project title to insert (NOT NULL in schema).

        Returns:
            int: the newly-created row id (project_id).
        """
        try:
            sql = "INSERT INTO Project (title) VALUES (?)"
            with _get_conn() as conn:
                cur = conn.execute(sql, (title,))
                return Project(project_id=cur.lastrowid, title=title)
        except Exception as e:
            raise e.with_traceback(e.__traceback__)
        return None
        
    def getProjectById(self, project_id: int) -> Optional[Project]:
        """Retrieve a project by id.

        Parameters:
            project_id (int): primary key of the project to fetch.

        Returns:
            Optional[Project]: `Project` instance if found, otherwise `None`.
        """
        try:
            sql = "SELECT project_id, title FROM Project WHERE project_id = ?"
            with _get_conn() as conn:
                cur = conn.execute(sql, (project_id,))
                row = cur.fetchone()
                if row:
                    return Project.from_row(dict(row))
        except Exception as e:
            raise e.with_traceback(e.__traceback__)
        return None

    def getAllProjects(self) -> List[Project]:
        """List all projects ordered by title.

        Returns:
            List[Project]: list of `Project` instances (empty list if none).
        """
        try:    
            sql = "SELECT project_id, title FROM Project ORDER BY title"
            with _get_conn() as conn:
                cur = conn.execute(sql)
                return [Project.from_row(dict(r)) for r in cur.fetchall()]
        except Exception as e:
            raise e.with_traceback(e.__traceback__)
        return []

    def updateProjectTitleById(self, project: Project) -> bool:
        """Update an existing project's title.

        Parameters:
            project (Project): `Project` instance with `project_id` and new `title`.

        Returns:
            bool: True if a row was updated, False otherwise.
        """
        try:
            sql = "UPDATE Project SET title = ? WHERE project_id = ?"
            with _get_conn() as conn:
                cur = conn.execute(sql, (project.title, project.project_id))
                return cur.rowcount > 0
        except Exception as e:
            raise e.with_traceback(e.__traceback__)
        return False
    
    def deleteProjectById(self, project_id: int) -> bool:
        """Delete a project by id.

        Parameters:
            project_id (int): id of the project to delete.

        Returns:
            bool: True if a row was deleted, False otherwise.
        """
        try:
            sql = "DELETE FROM Project WHERE project_id = ?"
            with _get_conn() as conn:
                cur = conn.execute(sql, (project_id,))
                return cur.rowcount > 0
        except Exception as e:
            raise e.with_traceback(e.__traceback__)
        return False