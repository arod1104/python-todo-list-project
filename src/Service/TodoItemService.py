class TodoItemService:
    def __init__(self):

from typing import List, Optional

from DAO.TodoItemDAO import TodoItemDAO
from DAO.ProjectDAO import ProjectDAO
from Models.TodoItem import TodoItem

class TodoItemService:
    def __init__(self):
        self.dao = TodoItemDAO()
        self.project_dao = ProjectDAO()

    def validate_priority(self, priority: int) -> bool:
        try:
            p = int(priority)
        except Exception:
            return False
        return 1 <= p <= 5

    def validate_description(self, description: str) -> bool:
        return bool(description and isinstance(description, str) and description.strip())

    def create_todo(self, title: str, description: str, priority: int, project_id: Optional[int] = None) -> Optional[TodoItem]:
        if not title or not isinstance(title, str) or not title.strip():
            return None
        if not self.validate_description(description):
            return None
        if not self.validate_priority(priority):
            return None
        # if project_id provided, verify it exists
        if project_id is not None and self.project_dao.get(project_id) is None:
            return None

        todo = TodoItem(todo_id=None, title=title.strip(), description=description.strip(), priority=int(priority), completed=False, project_id=project_id)
        new_id = self.dao.create(todo)
        return self.dao.get(new_id)

    def get_todo(self, todo_id: int) -> Optional[TodoItem]:
        return self.dao.get(todo_id)

    def list_todos(self, project_id: Optional[int] = None) -> List[TodoItem]:
        return self.dao.list_all(project_id)

    def update_todo(self, todo: TodoItem) -> bool:
        if not todo.title or not todo.title.strip():
            return False
        if not self.validate_description(todo.description):
            return False
        if not self.validate_priority(todo.priority):
            return False
        if todo.project_id is not None and self.project_dao.get(todo.project_id) is None:
            return False
        return self.dao.update(todo)

    def delete_todo(self, todo_id: int) -> bool:
        return self.dao.delete(todo_id)


    # Add todo item-related methods here