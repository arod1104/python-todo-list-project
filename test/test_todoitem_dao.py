import sys
import os

# ensure `src` is on the import path so Controller/Service packages resolve
ROOT = os.path.dirname(__file__)
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

import unittest
from src.DAO.TodoItemDAO import TodoItemDAO
from src.DAO.ProjectDAO import ProjectDAO
from src.Models.TodoItem import TodoItem
from src.Utils.db_connection import _get_conn

class TestTodoItemDAO(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the test database and seed data."""
        cls.dao = TodoItemDAO()
        cls.project_dao = ProjectDAO()
        with _get_conn() as conn:
            conn.execute("DROP TABLE IF EXISTS Todo_Item;")
            conn.execute("DROP TABLE IF EXISTS Project;")
            conn.execute("CREATE TABLE Project (project_id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL UNIQUE);")
            conn.execute("CREATE TABLE Todo_Item (todo_id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, description TEXT NOT NULL, priority INTEGER NOT NULL CHECK (priority BETWEEN 1 AND 5), completed TEXT NOT NULL CHECK (completed IN ('yes', 'no')), project_id INTEGER NOT NULL, FOREIGN KEY (project_id) REFERENCES Project(project_id) ON DELETE CASCADE);")
            conn.execute("INSERT INTO Project (title) VALUES ('Test Project');")

    def test_create_todo_item(self):
        """Test creating a new todo item."""
        todo = TodoItem(todo_id=None, title="Test Todo", description="Test Description", priority=3, completed="no", project_id=1)
        created_todo = self.dao.createTodoItem(todo)
        self.assertIsNotNone(created_todo)
        self.assertEqual(created_todo.title, "Test Todo")

    def test_get_todo_item_by_id(self):
        """Test retrieving a todo item by ID."""
        todo = self.dao.getTodoItemById(1)
        self.assertIsNotNone(todo)
        self.assertEqual(todo.title, "Test Todo")

    def test_get_all_todo_items(self):
        """Test retrieving all todo items."""
        todos = self.dao.getAllTodoItems()
        self.assertGreaterEqual(len(todos), 1)

    def test_update_todo_item(self):
        """Test updating a todo item."""
        todo = self.dao.getTodoItemById(1)
        todo.completed = "yes"
        result = self.dao.updateTodoItemById(todo)
        self.assertTrue(result)
        updated_todo = self.dao.getTodoItemById(1)
        self.assertEqual(updated_todo.completed, "yes")

    def test_delete_todo_item(self):
        """Test deleting a todo item."""
        result = self.dao.deleteTodoItemById(1)
        self.assertTrue(result)
        deleted_todo = self.dao.getTodoItemById(1)
        self.assertIsNone(deleted_todo)

if __name__ == "__main__":
    unittest.main()