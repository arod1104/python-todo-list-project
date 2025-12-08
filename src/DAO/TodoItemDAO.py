from typing import List, Optional

from Models.TodoItem import TodoItem
from Utils.db_connection import _get_conn


class TodoItemDAO:
    """Data access object for `Todo_Item` records."""

    def __init__(self):
        """Initialize the DAO instance.

        No parameters. Database path is determined from module-level settings.
        """
        pass

    def createTodoItem(self, item: TodoItem) -> Optional[TodoItem]:
        """Insert a new todo item into the database.

        Parameters:
            item (TodoItem): domain object containing todo fields. `todo_id` is ignored.

        Returns:
            Optional[TodoItem]: the created `TodoItem` with `todo_id` set if insertion succeeded, otherwise None.
        """
        try:
            sql = (
                "INSERT INTO Todo_Item (description, priority, completed, title, project_id) "
                "VALUES (?, ?, ?, ?, ?)"
            )
            with _get_conn() as conn:
                cur = conn.execute(sql, item.to_tuple_for_insert())
                if cur.lastrowid:
                    return TodoItem(
                        todo_id=cur.lastrowid,
                        title=item.title,
                        description=item.description,
                        priority=item.priority,
                        completed=item.completed,
                        project_id=item.project_id,
                    )
        except Exception as e:
            raise e.with_traceback(e.__traceback__)
        return None

    def getTodoItemById(self, todo_id: int) -> Optional[TodoItem]:
        """Fetch a todo item by its id.

        Parameters:
            todo_id (int): primary key of the todo item.

        Returns:
            Optional[TodoItem]: `TodoItem` if found, otherwise `None`.
        """
        try:
            sql = "SELECT todo_id, title, description, priority, completed, project_id, created_at FROM Todo_Item WHERE todo_id = ?"
            with _get_conn() as conn:
                cur = conn.execute(sql, (todo_id,))
                row = cur.fetchone()
                if row:
                    return TodoItem.from_row(dict(row))
        except Exception as e:
            raise e.with_traceback(e.__traceback__)
        return None

    def getAllTodoItemsByProjectId(self, project_id: int) -> List[TodoItem]:
        """List todo items, optionally filtered by project.

        Parameters:
            project_id (Optional[int]): if provided, only todos for this project are returned.

        Returns:
            List[TodoItem]: list of `TodoItem` instances (may be empty).
        """
        try:
            sql = "SELECT todo_id, title, description, priority, completed, project_id, created_at FROM Todo_Item WHERE project_id = ? ORDER BY priority ASC"
            params = (project_id,)
            with _get_conn() as conn:
                cur = conn.execute(sql, params)
                return [TodoItem.from_row(dict(r)) for r in cur.fetchall()]
        except Exception as e:
            raise e.with_traceback(e.__traceback__)
        return []
    
    def getAllTodoItemsByProjectTitle(self, project_title: str) -> List[TodoItem]:
        """List todo items, filtered by project title.

        Parameters:
            project_title (str): title of the project to filter todos.
        Returns:
            List[TodoItem]: list of `TodoItem` instances (may be empty).
        """
        try:
            sql = "SELECT ti.todo_id, ti.title, ti.description, ti.priority, ti.completed, ti.project_id, ti.title FROM Todo_Item ti JOIN Project p ON ti.project_id = p.project_id WHERE p.title = ? ORDER BY ti.priority ASC"
            params = (project_title,)
            with _get_conn() as conn:
                cur = conn.execute(sql, params)
                return [TodoItem.from_row(dict(r)) for r in cur.fetchall()]
        except Exception as e:
            raise e.with_traceback(e.__traceback__)
        return []

    def getAllTodoItems(self) -> List[TodoItem]:
        """List all todo items.
    
        Parameters:
            None
        Returns:
            List[TodoItem]: list of `TodoItem` instances (may be empty).
        """
        try:
            sql = "SELECT todo_id, description, priority, completed, project_id, title FROM Todo_Item ORDER BY priority ASC"
            with _get_conn() as conn:
                cur = conn.execute(sql)
                return [TodoItem.from_row(dict(r)) for r in cur.fetchall()]
        except Exception as e:
            raise e.with_traceback(e.__traceback__)
        return []

    def updateTodoItemById(self, item: TodoItem) -> bool:
        """Update an existing todo item.

        Parameters:
            item (TodoItem): `TodoItem` with `todo_id` set and updated fields.

        Returns:
            bool: True if a row was updated, False otherwise.
        """
        try:
            sql = (
                "UPDATE Todo_Item SET description = ?, priority = ?, completed = ?, title = ?, project_id = ? WHERE todo_id = ?"
            )
            with _get_conn() as conn:
                cur = conn.execute(sql, item.to_tuple_for_update())
                return cur.rowcount > 0
        except Exception as e:
            raise e.with_traceback(e.__traceback__)
        return False

    def deleteTodoItemById(self, todo_id: int) -> bool:
        """Delete a todo item by id.

        Parameters:
            todo_id (int): id of the todo to delete.

        Returns:
            bool: True if a row was deleted, False otherwise.
        """
        try:
            sql = "DELETE FROM Todo_Item WHERE todo_id = ?"
            with _get_conn() as conn:
                cur = conn.execute(sql, (todo_id,))
                return cur.rowcount > 0
        except Exception as e:
            raise e.with_traceback(e.__traceback__)
        return False
    