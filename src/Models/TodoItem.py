from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from datetime import datetime


@dataclass
class TodoItem:
    todo_id: Optional[int]
    title: str
    description: str
    priority: int
    completed: bool = False
    project_id: Optional[int] = None
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "todo_id": self.todo_id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "completed": "yes" if self.completed else "no",
            "project_id": self.project_id,
            "created_at": self.created_at,
        }

    def to_tuple_for_insert(self):
        return (self.title, self.description, self.priority, "yes" if self.completed else "no", self.project_id, self.created_at)

    def to_tuple_for_update(self):
        return (self.title, self.description, self.priority, "yes" if self.completed else "no", self.project_id, self.created_at, self.todo_id)

    @classmethod
    def from_row(cls, row: Dict[str, Any]) -> "TodoItem":
        return cls(
            todo_id=row.get("todo_id") or row.get("id"),
            title=row.get("title") or "",
            description=row.get("description") or "",
            priority=int(row.get("priority") or 3),
            completed=(row.get("completed") == "yes" or bool(row.get("completed")) and str(row.get("completed")).lower() in ("1","true","yes")),
            project_id=row.get("project_id"),
            created_at=row.get("created_at") or datetime.utcnow().isoformat(),
        )

    def __str__(self) -> str:
        return f"TodoItem(id={self.todo_id}, title={self.title}, priority={self.priority}, completed={self.completed})"

