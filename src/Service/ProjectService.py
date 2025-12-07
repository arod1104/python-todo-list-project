from typing import List, Optional

from DAO.ProjectDAO import ProjectDAO
from Models.Project import Project


class ProjectService:
    def __init__(self):
        self.dao = ProjectDAO()

    def validate_title(self, title: str) -> bool:
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
        if not self.validate_title(title):
            return None
        return self.dao.addProject(title.strip())

    def getProject(self, project_id: int) -> Optional[Project]:
        return self.dao.getProjectById(project_id)

    def listProjects(self) -> List[Project]:
        return self.dao.getAllProjects()

    def updateProject(self, project: Project) -> bool:
        if not self.validate_title(project.title):
            return False
        return self.dao.updateProjectTitleById(project)

    def deleteProject(self, project_id: int) -> bool:
        return self.dao.deleteProjectById(project_id)