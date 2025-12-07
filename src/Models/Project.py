from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class Project:
    project_id: Optional[int]
    title: str

    def to_dict(self) -> Dict[str, Any]:
        return {"project_id": self.project_id, "title": self.title}

    @classmethod
    def from_row(cls, row: Dict[str, Any]) -> "Project":
        return cls(project_id=row.get("project_id"), title=row.get("title") or "")

    def __str__(self) -> str:
        return f"Project(id={self.project_id}, title={self.title})"
