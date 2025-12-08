import sys
import os

# ensure `src` is on the import path so Controller/Service packages resolve
ROOT = os.path.dirname(__file__)
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

import unittest
from src.Service.ProjectService import ProjectService
from src.Models.Project import Project
from src.Utils.db_connection import _get_conn

class TestProjectService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the test database and seed data."""
        cls.service = ProjectService()
        with _get_conn() as conn:
            conn.execute("DROP TABLE IF EXISTS Project;")
            conn.execute("CREATE TABLE Project (project_id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL UNIQUE);")
            conn.execute("INSERT INTO Project (title) VALUES ('Test Project 1');")

    def test_create_project(self):
        """Test creating a new project."""
        project = self.service.createProject("New Test Project")
        self.assertIsNotNone(project)
        self.assertEqual(project.title, "New Test Project")

    def test_get_project(self):
        """Test retrieving a project by ID."""
        project = self.service.getProject(1)
        self.assertIsNotNone(project)
        self.assertEqual(project.title, "Test Project 1")

    def test_get_all_projects(self):
        """Test retrieving all projects."""
        projects = self.service.getAllProjects()
        self.assertGreaterEqual(len(projects), 1)

    def test_update_project(self):
        """Test updating a project's title."""
        project = Project(project_id=1, title="Updated Project Title")
        result = self.service.updateProject(project)
        self.assertTrue(result)
        updated_project = self.service.getProject(1)
        self.assertEqual(updated_project.title, "Updated Project Title")

    def test_delete_project(self):
        """Test deleting a project by ID."""
        result = self.service.deleteProject(1)
        self.assertTrue(result)
        deleted_project = self.service.getProject(1)
        self.assertIsNone(deleted_project)

if __name__ == "__main__":
    unittest.main()