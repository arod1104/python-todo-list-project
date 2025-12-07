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
            projects list            List all projects
            projects create          Create a new project
            projects delete <id>     Delete a project by id

            Todos:
            todos list [project_id]  List todos (optionally for a project)
            todos add                Add a todo (interactive prompts)
            todos complete <id>      Mark todo completed
            todos delete <id>        Delete a todo by id
            """
        print(help_text)

    def _prompt(self, prompt: str, default: str = "") -> str:
        if default is None:
            return input(prompt).strip()
        v = input(f"{prompt} [{default}] ").strip()
        return v or default

    def _create_project_flow(self):
        title = self._prompt("Project title: ")
        proj = self.projectService.createProject(title)
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
        title = self._prompt("Todo title: ")
        description = self._prompt("Description: ")
        while True:
            priority_raw = self._prompt("Priority (1-5, default 3): ", "3")
            try:
                priority = int(priority_raw)
            except Exception:
                print("Priority must be an integer 1-5")
                continue
            if 1 <= priority <= 5:
                break
            print("Priority must be between 1 and 5")

        self._list_projects()
        proj_raw = self._prompt("Project id (enter 0 for all todo items): ", "").strip()
        while True:
            try:
                proj_id = int(proj_raw)
                todo = self.todoItemService.createTodoItem(title=title, description=description, priority=priority, project_id=proj_id)
                if todo:
                    print(f"Created todo: {todo}")
                else:
                    print("Failed to create todo. Check inputs and project id.")
            except ValueError:
                print("Project id must be a numeric value.")
                continue
            break

    def _list_todos(self, project_id: Optional[int] = None):
        if project_id is None:
            todos = self.todoItemService.getAllTodoItems()
        else:
            todos = self.todoItemService.getAllTodoItemsByProjectId(project_id)
        if not todos:
            print("No todo items found")
            return
        print("Todos:")
        for t in todos:
            status = "yes" if t.completed else "no"
            print(f"  {t.todo_id}: [{status}] {t.title} (priority={t.priority}) project={t.project_id}")

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

    def _delete_project(self, project_id: int):
        ok = self.projectService.deleteProject(project_id)
        print("Deleted project" if ok else "Not found or failed")

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
                    self._create_project_flow()
                elif len(parts) >= 3 and parts[1] == "delete":
                    try:
                        pid = int(parts[2])
                    except Exception:
                        print("Provide a numeric project id to delete")
                        continue
                    self._delete_project(pid)
                else:
                    print("Unknown projects command. Use 'projects list' or 'projects create' or 'projects delete <id>'")
                continue

            if cmd == "todos":
                if len(parts) >= 2 and parts[1] == "list":
                    if len(parts) == 3:
                        try:
                            pid = int(parts[2])
                        except Exception:
                            print("project id must be numeric")
                            continue
                        self._list_todos(project_id=pid)
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
                    print("Unknown todos command. Use 'todos list [project_id]', 'todos add', 'todos complete <id>', or 'todos delete <id>'")
                continue

            print("Unknown command. Type 'help' for available commands")

