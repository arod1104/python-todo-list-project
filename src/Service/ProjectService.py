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

    def create_project(self, title: str) -> Optional[Project]:
        if not self.validate_title(title):
            return None
        project_id = self.dao.create(title.strip())
        return self.dao.get(project_id)

    def get_project(self, project_id: int) -> Optional[Project]:
        return self.dao.get(project_id)

    def list_projects(self) -> List[Project]:
        return self.dao.list_all()

    def update_project(self, project: Project) -> bool:
        if not self.validate_title(project.title):
            return False
        return self.dao.update(project)

    def delete_project(self, project_id: int) -> bool:
        return self.dao.delete(project_id)
