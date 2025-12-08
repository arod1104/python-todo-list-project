import sys
import os

# ensure `src` is on the import path so Controller/Service packages resolve
ROOT = os.path.dirname(__file__)
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

import unittest
from src.DAO.ProjectDAO import ProjectDAO
from src.Models.Project import Project
from src.Utils.db_connection import _get_conn

class TestProjectDAO(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the test database and seed data."""
        cls.dao = ProjectDAO()
        with _get_conn() as conn:
            conn.execute("DROP TABLE IF EXISTS Project;")
            conn.execute("CREATE TABLE Project (project_id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL UNIQUE);")
            conn.execute("INSERT INTO Project (title) VALUES ('Test Project 1');")
            conn.execute("INSERT INTO Project (title) VALUES ('Test Project 2');")

    def test_create_project(self):
        """Test creating a new project."""
        project = self.dao.createProject("New Test Project")
        self.assertIsNotNone(project)
        self.assertEqual(project.title, "New Test Project")

    def test_get_project_by_id(self):
        """Test retrieving a project by ID."""
        project = self.dao.getProjectById(1)
        self.assertIsNotNone(project)
        self.assertEqual(project.title, "Test Project 1")

    def test_get_all_projects(self):
        """Test retrieving all projects."""
        projects = self.dao.getAllProjects()
        self.assertGreaterEqual(len(projects), 2)

    def test_update_project_title(self):
        """Test updating a project's title."""
        project = Project(project_id=1, title="Updated Project Title")
        result = self.dao.updateProjectTitleById(project)
        self.assertTrue(result)
        updated_project = self.dao.getProjectById(1)
        self.assertEqual(updated_project.title, "Updated Project Title")

    def test_delete_project_by_id(self):
        """Test deleting a project by ID."""
        result = self.dao.deleteProjectById(1)
        self.assertTrue(result)
        deleted_project = self.dao.getProjectById(1)
        self.assertIsNone(deleted_project)

if __name__ == "__main__":
    unittest.main()