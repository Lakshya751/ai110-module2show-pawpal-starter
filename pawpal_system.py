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
        if self.frequency == "daily":
            delta = timedelta(days=1)
        elif self.frequency == "weekly":
            delta = timedelta(weeks=1)
        else:
            return None
        base = self.due_date or date.today()
        return Task(
            description=self.description,
            time=self.time,
            frequency=self.frequency,
            completed=False,
            due_date=base + delta,
        )


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
        """Return (pet, task) pairs sorted chronologically by task time.

        Times are zero-padded "HH:MM" strings, so a plain string sort is already
        chronological (e.g. "08:00" < "09:30" < "18:00").
        """
        return sorted(self.all_tasks(), key=lambda pair: pair[1].time)

    def filter_by_status(self, completed: bool) -> List[tuple]:
        """Return (pet, task) pairs matching the given completion status."""
        return [(pet, task) for pet, task in self.all_tasks() if task.completed == completed]

    def filter_by_pet(self, pet_name: str) -> List[tuple]:
        """Return (pet, task) pairs belonging to the named pet."""
        return [(pet, task) for pet, task in self.all_tasks() if pet.name == pet_name]

    def mark_task_complete(self, task: Task) -> Optional[Task]:
        """Mark a task complete; if recurring, create and attach its next occurrence.

        Returns the newly created next-occurrence Task, or None for one-off tasks.
        """
        task.mark_complete()
        next_task = task.next_occurrence()
        if next_task is None:
            return None
        # Attach the new occurrence to whichever pet owns the completed task.
        for pet in self.owner.pets:
            if task in pet.tasks:
                pet.add_task(next_task)
                break
        return next_task

    def detect_conflicts(self) -> List[str]:
        """Return warning strings for tasks scheduled at the same time.

        Lightweight strategy: group tasks by their exact "HH:MM" time and warn about
        any time slot that holds two or more tasks. Returns messages rather than
        raising, so callers can display them without crashing.
        """
        by_time: dict = {}
        for pet, task in self.all_tasks():
            by_time.setdefault(task.time, []).append(f"{task.description} ({pet.name})")

        warnings = []
        for time in sorted(by_time):
            entries = by_time[time]
            if len(entries) > 1:
                warnings.append(f"Conflict at {time}: " + ", ".join(entries))
        return warnings

    def todays_schedule(self) -> str:
        """Return a readable, time-sorted summary of today's tasks plus conflicts."""
        pairs = self.sort_by_time()
        if not pairs:
            return "Today's Schedule:\n  (no tasks yet)"

        lines = ["Today's Schedule:"]
        for pet, task in pairs:
            status = "done" if task.completed else "todo"
            lines.append(
                f"  {task.time}  {task.description} "
                f"({pet.name}) [{task.frequency}] [{status}]"
            )

        conflicts = self.detect_conflicts()
        if conflicts:
            lines.append("")
            lines.append("⚠️  Conflicts:")
            for warning in conflicts:
                lines.append(f"  - {warning}")

        return "\n".join(lines)
