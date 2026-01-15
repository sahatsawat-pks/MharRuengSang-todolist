"""
Data models for the Python CLI To-Do List Application.
"""

from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4
from datetime import datetime

class Priority(Enum):
    HIGH = "HIGH"
    MID = "MID"
    LOW = "LOW"

class Status(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"

@dataclass
class TodoItem:
    id: str = field(default_factory=lambda: str(uuid4()))
    title: str = ""
    details: str = ""
    priority: Priority = Priority.MID
    status: Status = Status.PENDING
    owner: str = ""
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
