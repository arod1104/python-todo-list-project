# python-todo-list-project

A Todo list application written in Python with a SQLite database backend. The application allows users to create projects and add todo items to those projects. Users can list, complete, and delete todo items, as well as manage projects.

## Project Setup on Linux

Follow these steps to set up and run the project on a Linux environment:

### Install Dependencies

Run the following commands to install the required dependencies:

```bash
sudo apt update
sudo apt install -y python3 python3.8-venv sqlite3
```

Alternatively, you can use the provided script to install dependencies:

```bash
sudo ./scripts/install_dependencies.sh
```

### Set Up the Project

1. Clone the repository:

```bash
   git clone <repository-url>
   cd python-todo-list-project
```

2. Run the setup script to create a virtual environment, install Python dependencies, and initialize the database:

```bash
   ./scripts/setup.sh
```

3.  Afterwars, start the virtual environment to ensure the correct Python packages are used:

```bash
   source .venv/bin/activate
```

### Running the Application

Once the virtual enviroment is activated, run the application with the following command:

```bash
python3 main.py
```

### Running Tests

To run the tests, use the following command:

```bash
python3 -m unittest discover -s test
```

### Test Coverage

The following areas are covered by the tests:

- **DAO Tests**:
  - `test_project_dao.py`: Tests for `ProjectDAO`.
  - `test_todoitem_dao.py`: Tests for `TodoItemDAO`.
- **Service Tests**:
  - `test_project_service.py`: Tests for `ProjectService`.
  - `test_todoitem_service.py`: Tests for `TodoItemService`.

These tests ensure that the database operations and business logic work as expected.

## Design Document

### 1. Approach and Design

- **Objective**: Create a command-line Todo list application with support for projects and tasks.
- **Architecture**: The application follows a modular design with clear separation of concerns:
  - **Controller**: Handles user input and application flow.
  - **Service**: Contains business logic.
  - **DAO (Data Access Object)**: Manages database interactions.
  - **Models**: Defines data structures.
- **Database**: SQLite is used for data persistence, with tables for `Project` and `Todo_Item`.
- **Features**:
  - Create, list, and delete projects.
  - Add, list, complete, and delete todos.
  - Cascading deletes: Deleting a project removes its associated todos.

### 2. Key Files and Folders

- **`main.py`**: Entry point for the application.
- **`src/Controller/TodoListController.py`**: Handles user commands and application flow.
- **`src/Service/`**: Contains `ProjectService.py` and `TodoItemService.py` for business logic.
- **`src/DAO/`**: Contains `ProjectDAO.py` and `TodoItemDAO.py` for database operations.
- **`src/Models/`**: Defines `Project` and `TodoItem` data models.
- **`src/Resources/TodoListSetup.sql`**: SQLite schema and seed data.
- **`scripts/`**: Contains setup scripts:
  - `setup.sh`: Sets up the virtual environment and initializes the database.
  - `install_dependencies.sh`: Installs system dependencies.

### 3. Process to Run, Test, and Verify

- **Run the Application**:

  1. Start the application:
     ```bash
     python3 main.py
     ```
  2. Use the following commands in the application:
     - `help`: Display available commands.
     - `projects list`: List all projects.
     - `projects create <project_title>`: Create a new project.
     - `projects delete <project_title>`: Delete a project.
     - `todos list [project_title]`: List todos (optionally for a project).
     - `todos add`: Add a new todo.
     - `todos complete <todo_id>`: Mark a todo as completed.
     - `todos delete <todo_id>`: Delete a todo.

- **Test the Application**:
  1. Verify that projects and todos are created, listed, and deleted as expected.
  2. Ensure cascading deletes work (deleting a project removes its todos).

### 4. Test Data and Seed Data

- **Seed Data**:
  - The `src/Resources/TodoListSetup.sql` file includes seed data for testing:
    - Projects: `General`, `Work`, `Personal`.
    - Todos: Example tasks for each project.
- **Testing**:
  - Use the seed data to verify the application functionality.
  - Add new projects and todos to test CRUD operations.

## Bullet Points for Slideshow

### 1. Approach and Design

- Objective: Command-line Todo list application.
- Modular architecture: Controller, Service, DAO, Models.
- SQLite database with `Project` and `Todo_Item` tables.
- Features: CRUD operations for projects and todos, cascading deletes.

### 2. Key Files and Folders

- `main.py`: Entry point.
- `src/Controller/`: Handles user commands.
- `src/Service/`: Business logic.
- `src/DAO/`: Database operations.
- `src/Models/`: Data models.
- `src/Resources/TodoListSetup.sql`: Schema and seed data.
- `scripts/`: Setup scripts.

### 3. Process to Run, Test, and Verify

- Run the application: `python3 main.py`.
- Commands:
  - `help`: Display commands.
  - `projects list/create/delete`.
  - `todos list/add/complete/delete`.
- Test cascading deletes and CRUD operations.

### 4. Test Data and Seed Data

- Seed data in `TodoListSetup.sql`:
  - Projects: `General`, `Work`, `Personal`.
  - Todos: Example tasks for each project.
- Add new projects and todos to test functionality.

---
