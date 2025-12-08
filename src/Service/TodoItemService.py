from typing import List, Optional
from datetime import datetime, timezone

from DAO.TodoItemDAO import TodoItemDAO
from Service.ProjectService import ProjectService
from Models.TodoItem import TodoItem

class TodoItemService:
    def __init__(self):
        self.dao = TodoItemDAO()
        self.project_service = ProjectService()

    def validate_priority(self, priority: int) -> bool:
        """
        Validates the priority of a todo item.

        Parameters:
        priority (int): The priority level to validate (1-5).

        Returns:
        bool: True if the priority is valid, False otherwise.
        """
        try:
            p = int(priority)
        except Exception:
            return False
        return 1 <= p <= 5

    def validate_description(self, description: str) -> bool:
        """
        Validates the description of a todo item.

        Parameters:
        description (str): The description to validate.

        Returns:
        bool: True if the description is valid, False otherwise.
        """
        return bool(description and isinstance(description, str) and description.strip())

    def createTodoItem(self, title: str, description: str, priority: int, project_id: Optional[int]) -> Optional[TodoItem]:
        """
        Creates a new todo item.

        Parameters:
        title (str): The title of the todo item.
        description (str): The description of the todo item.
        priority (int): The priority level of the todo item (1-5).
        project_id (int): The ID of the associated project.

        Returns:
        Optional[TodoItem]: The created TodoItem object if successful, None otherwise.
        """
        if not title or not isinstance(title, str) or not title.strip():
            return None
        if not self.validate_description(description):
            return None
        if not self.validate_priority(priority):
            return None
        # if project_id provided, verify it exists
        if self.project_service.getProjectByTitle(title) is None:
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
        """
        Retrieves a todo item by its ID.

        Parameters:
        todo_id (int): The ID of the todo item to retrieve.

        Returns:
        Optional[TodoItem]: The TodoItem object if found, None otherwise.
        """
        return self.dao.getTodoItemById(todo_id)
    
    def getAllTodoItemsByProjectId(self, project_id: int) -> List[TodoItem]:
        """
        Retrieves all todo items associated with a specific project.

        Parameters:
        project_id (int): The ID of the project.

        Returns:
        List[TodoItem]: A list of TodoItem objects associated with the project.
        """
        return self.dao.getAllTodoItemsByProjectId(project_id)

    def getAllTodoItemsByProjectTitle(self, project_title: str) -> List[TodoItem]:
        """
        Retrieves all todo items associated with a specific project title.

        Parameters:
        project_title (str): The title of the project.

        Returns:
        List[TodoItem]: A list of TodoItem objects associated with the project.
        """
        return self.dao.getAllTodoItemsByProjectTitle(project_title)
    
    def getAllTodoItems(self) -> List[TodoItem]:
        """
        Retrieves all todo items.

        Returns:
        List[TodoItem]: A list of all TodoItem objects.
        """
        return self.dao.getAllTodoItems()

    def updateTodoItem(self, todo: TodoItem) -> bool:
        """
        Updates an existing todo item.

        Parameters:
        todo (TodoItem): The TodoItem object containing updated information.

        Returns:
        bool: True if the update was successful, False otherwise.
        """
        if not todo.title or not todo.title.strip():
            return False
        if not self.validate_description(todo.description):
            return False
        if not self.validate_priority(todo.priority):
            return False
        if todo.project_id is not None and self.project_service.getProjectByTitle(todo.title) is None:
            return False
        return self.dao.updateTodoItemById(todo)

    def deleteTodoItem(self, todo_id: int) -> bool:
        """
        Deletes a todo item by its ID.

        Parameters:
        todo_id (int): The ID of the todo item to delete.

        Returns:
        bool: True if the deletion was successful, False otherwise.
        """
        return self.dao.deleteTodoItemById(todo_id)
