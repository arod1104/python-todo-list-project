from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from datetime import datetime, timezone


@dataclass
class TodoItem:
    todo_id: Optional[int]
    description: str
    priority: int
    title: str
    completed: bool = False
    project_id: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "todo_id": self.todo_id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "completed": "yes" if self.completed else "no",
            "project_id": self.project_id,
        }

    def to_tuple_for_insert(self):
        return (self.description, self.priority, "yes" if self.completed else "no", self.title, self.project_id)

    def to_tuple_for_update(self):
        return (self.description, self.priority, "yes" if self.completed else "no", self.title, self.project_id, self.todo_id)

    @classmethod
    def from_row(cls, row: Dict[str, Any]) -> "TodoItem":
        return cls(
            todo_id=row.get("todo_id"),
            title=row.get("title") or "",
            description=row.get("description") or "",
            priority=int(row.get("priority") or 3),
            completed=(row.get("completed") == "yes" or bool(row.get("completed")) and str(row.get("completed")).lower() in ("1","true","yes")),
            project_id=row.get("project_id"),
        )

    def __str__(self) -> str:
        return f"TodoItem(id={self.todo_id}, title={self.title}, priority={self.priority}, completed={self.completed})"

