from typing import List, Optional

from DAO.ProjectDAO import ProjectDAO
from Models.Project import Project


class ProjectService:
    def __init__(self):
        self.dao = ProjectDAO()

    def validate_title(self, title: str) -> bool:
        """
        Validates the title of a project.

        Parameters:
        title (str): The title of the project to validate.

        Returns:
        bool: True if the title is valid, False otherwise.
        """
        if not title or not isinstance(title, str):
            return False
        # simple length check and disallow only whitespace
        if not title.strip():
            return False
        # optional: restrict weird characters
        if len(title.strip()) > 200:
            return False
        return True

    def createProject(self, title: str) -> Optional[Project]:
        """
        Creates a new project with the given title.

        Parameters:
        title (str): The title of the project to create.

        Returns:
        Optional[Project]: The created Project object if successful, None otherwise.
        """
        if not self.validate_title(title):
            return None
        return self.dao.addProject(title.strip())

    def getProject(self, project_id: int) -> Optional[Project]:
        """
        Retrieves a project by its ID.

        Parameters:
        project_id (int): The ID of the project to retrieve.

        Returns:
        Optional[Project]: The Project object if found, None otherwise.
        """
        return self.dao.getProjectById(project_id)
    
    def getAllProjects(self) -> List[Project]:
        """
        Retrieves all projects.

        Returns:
        List[Project]: A list of all Project objects.
        """
        return self.dao.getAllProjects()

    def listProjects(self) -> List[Project]:
        """
        Retrieves all projects (alias for getAllProjects).

        Returns:
        List[Project]: A list of all Project objects.
        """
        return self.dao.getAllProjects()

    def updateProject(self, project: Project) -> bool:
        """
        Updates the title of an existing project.

        Parameters:
        project (Project): The Project object containing the updated title and ID.

        Returns:
        bool: True if the update was successful, False otherwise.
        """
        if not self.validate_title(project.title):
            return False
        return self.dao.updateProjectTitleById(project)

    def deleteProject(self, project_id: int) -> bool:
        """
        Deletes a project by its ID.

        Parameters:
        project_id (int): The ID of the project to delete.

        Returns:
        bool: True if the deletion was successful, False otherwise.
        """
        return self.dao.deleteProjectById(project_id)