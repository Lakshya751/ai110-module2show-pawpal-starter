"""PawPal+ logic layer.

Backend classes for the PawPal+ pet-care planner. This is the SKELETON generated
from diagrams/uml_draft.mmd (Phase 1, Step 4): class names, attributes, and empty
method stubs. Method bodies are implemented in Phase 2.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List, Optional


@dataclass
class Task:
    """A single pet-care activity (skeleton)."""

    description: str
    time: str  # "HH:MM"
    frequency: str = "once"  # "once" | "daily" | "weekly"
    completed: bool = False
    due_date: Optional[date] = None

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def next_occurrence(self) -> Optional["Task"]:
        """Return the next Task for a recurring task, or None if not recurring."""
        # Implemented in Phase 4 (recurring tasks).
        raise NotImplementedError


@dataclass
class Pet:
    """A pet and its list of care tasks (skeleton)."""

    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet."""
        self.tasks.append(task)


@dataclass
class Owner:
    """An owner who manages one or more pets (skeleton)."""

    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet under this owner."""
        self.pets.append(pet)

    def all_tasks(self) -> List[tuple]:
        """Return every (pet, task) pair across all of this owner's pets."""
        return [(pet, task) for pet in self.pets for task in pet.tasks]


class Scheduler:
    """The 'brain': organizes tasks across an owner's pets (skeleton)."""

    def __init__(self, owner: Owner) -> None:
        self.owner = owner

    def all_tasks(self) -> List[tuple]:
        """Return every (pet, task) pair for the owner."""
        return self.owner.all_tasks()

    def sort_by_time(self) -> List[tuple]:
        """Return (pet, task) pairs sorted chronologically by task time."""
        raise NotImplementedError

    def filter_by_status(self, completed: bool) -> List[tuple]:
        """Return (pet, task) pairs matching the given completion status."""
        raise NotImplementedError

    def filter_by_pet(self, pet_name: str) -> List[tuple]:
        """Return (pet, task) pairs belonging to the named pet."""
        raise NotImplementedError

    def mark_task_complete(self, task: Task) -> Optional[Task]:
        """Mark a task complete; create/attach its next occurrence if recurring."""
        raise NotImplementedError

    def detect_conflicts(self) -> List[str]:
        """Return warning strings for tasks scheduled at the same time."""
        raise NotImplementedError

    def todays_schedule(self) -> str:
        """Return a readable summary of today's tasks (upgraded in Phase 4)."""
        pairs = self.all_tasks()
        if not pairs:
            return "Today's Schedule:\n  (no tasks yet)"

        lines = ["Today's Schedule:"]
        for pet, task in pairs:
            status = "done" if task.completed else "todo"
            lines.append(
                f"  {task.time}  {task.description} "
                f"({pet.name}) [{task.frequency}] [{status}]"
            )
        return "\n".join(lines)
