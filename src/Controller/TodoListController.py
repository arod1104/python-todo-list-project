from Service.ProjectService import ProjectService
from Service.TodoItemService import TodoItemService

class TodoListController:
    def __init__(self):
        this.projectService = ProjectService()
        this.todoItemService = TodoItemService()
        

    def display_help(self):
        help_text = """
        Todo List Application Commands:
        - help/h/? : Display this help message
        - quit/exit : Exit the application
        """
        print(help_text)


    # this method wull start the application and run the main loop
    def run(self):
        print("Todo List Application started.")

        while True:
            command = input("Enter command (help/h/? for help, quit/exit to exit the application)> ").strip().lower()

            if command in ['quit', 'exit']:
                print("Exiting the application.")
                break
            elif command in ['help', 'h', '?']:
                self.display_help()
            else:

