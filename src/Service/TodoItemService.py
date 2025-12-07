from typing import List, Optional
from datetime import datetime, timezone

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

    def createTodoItem(self, title: str, description: str, priority: int, project_id: int) -> Optional[TodoItem]:
        if not title or not isinstance(title, str) or not title.strip():
            return None
        if not self.validate_description(description):
            return None
        if not self.validate_priority(priority):
            return None
        # if project_id provided, verify it exists
        if self.project_dao.getProjectById(project_id) is None:
            return None

        todoObj = TodoItem(
            todo_id=None,
            title=title.strip(),
            description=description.strip(),
            priority=int(priority),
            completed=False,
            project_id=project_id,
            created_at=datetime.now(timezone.utc).isoformat()
        )
        return self.dao.createTodoItem(todoObj)

    def getTodoItemById(self, todo_id: int) -> Optional[TodoItem]:
        return self.dao.getTodoItemById(todo_id)
    
    def getAllTodoItems(self, project_id:int) -> List[TodoItem]:
        return self.dao.getAllTodoItemsByProjectId(project_id)

    def updateTodoItem(self, todo: TodoItem) -> bool:
        if not todo.title or not todo.title.strip():
            return False
        if not self.validate_description(todo.description):
            return False
        if not self.validate_priority(todo.priority):
            return False
        if todo.project_id is not None and self.project_dao.getProjectById(todo.project_id) is None:
            return False
        return self.dao.updateTodoItemById(todo)

    def deleteTodoItem(self, todo_id: int) -> bool:
        return self.dao.deleteTodoItemById(todo_id)
