from typing import Optional

from Service.ProjectService import ProjectService
from Service.TodoItemService import TodoItemService


class TodoListController:
    def __init__(self):
        self.projectService = ProjectService()
        self.todoItemService = TodoItemService()

    def display_help(self):
        help_text = """
            Todo List Application Commands:
            help/h/?                 Display this help message
            quit/exit                Exit the application

            Projects:
            projects list                     List all projects
            projects create <project_title>   Create a new project
            projects delete <project_title>   Delete a project by title

            Todos:
            todos list <project_title>  List todos (optionally for a project)
            todos add                Add a todo (interactive prompts)
            todos complete <todo_id>      Mark todo completed
            todos delete <todo_id>        Delete a todo by id
            """
        print(help_text)

    def _prompt(self, prompt: str, default: str = "") -> str:
        if default is None:
            return input(prompt).strip()
        v = input(f"{prompt} [{default}] ").strip()
        return v or default

    def _create_project_flow(self, project_title: str):
        proj = self.projectService.createProject(project_title)
        if proj:
            print(f"Created: {proj}")
        else:
            print("Failed to create project. Title may be invalid.")

    def _list_projects(self):
        projects = self.projectService.getAllProjects()
        if not projects:
            print("No projects found")
            return
        print("Projects:")
        for p in projects:
            print(f"  {p.project_id}: {p.title}")

    def _add_todo_flow(self):
        project_title = ""
        while True:
            project_title = self._prompt("Enter Project Title: ")
            if project_title and isinstance(project_title, str) and project_title.strip():
                project = self.projectService.getProjectByTitle(project_title)
                if project:
                    break
                else:
                    print("Project not found. Please enter a valid project title.")
            else:
                print("Project title cannot be empty.")

        description = self._prompt("Description: ")

        while True:
            priority_raw = self._prompt("Priority (1-5, default 3): ", "3")
            try:
                priority = int(priority_raw)
            except ValueError:
                print("Priority must be an integer between 1 and 5.")
                continue
            if 1 <= priority <= 5:
                break
            print("Priority must be between 1 and 5.")

        todo = self.todoItemService.createTodoItem(
            title=project.title,
            description=description,
            priority=priority,
            project_id=project.project_id
        )
        if todo:
            print(f"Created todo: {todo}")
        else:
            print("Failed to create todo. Check inputs and try again.")

    def _list_todos(self, project_title: Optional[str] = None):
        if project_title:
            project = self.projectService.getProjectByTitle(project_title)
            if not project:
                print("Project not found")
                return
            todos = self.todoItemService.getAllTodoItemsByProjectTitle(project.title)
        else:
            todos = self.todoItemService.getAllTodoItems()

        if not todos:
            print("No todo items found")
            return

        print("Todos:")
        print("Todo id; [status] (priority) description Project: project_title")
        print()
        for t in todos:
            status = "x" if t.completed else " "
            print(f"  id: {t.todo_id}: [{status}] (priority: {t.priority}) {t.description} Project: {t.title or 'N/A'}")

    def _complete_todo(self, todo_id: int):
        todo = self.todoItemService.getTodoItemById(todo_id)
        if not todo:
            print("Todo not found")
            return
        todo.completed = True
        ok = self.todoItemService.updateTodoItem(todo)
        print("Marked completed" if ok else "Failed to update todo")

    def _delete_todo(self, todo_id: int):
        ok = self.todoItemService.deleteTodoItem(todo_id)
        print("Deleted" if ok else "Not found or failed")

    def _delete_project(self, project_title: str):
        project = self.projectService.getProjectByTitle(project_title)
        if not project:
            print("Project not found")
            return
        ok = self.projectService.deleteProjectByTitle(project_title)
        print("Deleted project" if ok else "Failed to delete project")

    # main loop
    def run(self):
        print("Todo List Application started. Type 'help/h/?' for commands")

        while True:
            try:
                command = input(
                    "cmd> "
                ).strip()
            except (EOFError, KeyboardInterrupt):
                print("\nExiting")
                break

            if not command:
                continue

            parts = command.split()
            cmd = parts[0].lower()

            if cmd in ["quit", "exit"]:
                print("Exiting the application.")
                break
            if cmd in ["help", "h", "?"]:
                self.display_help()
                continue

            if cmd == "projects":
                if len(parts) >= 2 and parts[1] == "list":
                    self._list_projects()
                elif len(parts) >= 2 and parts[1] == "create":
                    if len(parts) >= 3:
                        self._create_project_flow(parts[2])
                    else:
                        print("Error: No project title provided.")
                elif len(parts) >= 3 and parts[1] == "delete":
                    self._delete_project(parts[2])
                else:
                    print("Unknown projects command. Use 'projects list' or 'projects create' or 'projects delete <title>'")
                continue

            if cmd == "todos":
                if len(parts) >= 2 and parts[1] == "list":
                    if len(parts) == 3:
                        self._list_todos(project_title=parts[2])
                    else:
                        self._list_todos()
                elif len(parts) >= 2 and parts[1] == "add":
                    self._add_todo_flow()
                elif len(parts) >= 3 and parts[1] == "complete":
                    try:
                        tid = int(parts[2])
                    except Exception:
                        print("todo id must be numeric")
                        continue
                    self._complete_todo(tid)
                elif len(parts) >= 3 and parts[1] == "delete":
                    try:
                        tid = int(parts[2])
                    except Exception:
                        print("todo id must be numeric")
                        continue
                    self._delete_todo(tid)
                else:
                    print("Unknown todos command. Use 'todos list [project_title]', 'todos add', 'todos complete <id>', or 'todos delete <id>'")
                continue

            print("Unknown command. Type 'help' for available commands")

