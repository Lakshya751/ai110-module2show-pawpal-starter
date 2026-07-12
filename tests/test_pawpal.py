"""Tests for the PawPal+ logic layer (pawpal_system.py)."""

from pawpal_system import Owner, Pet, Task


# --- Phase 2: core behavior -------------------------------------------------

def test_mark_complete_changes_status():
    """mark_complete() flips a task's completed flag to True."""
    task = Task("Morning walk", "08:00")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_adding_task_increases_pet_task_count():
    """Adding a task to a pet grows that pet's task list by one."""
    pet = Pet("Biscuit", "dog")
    assert len(pet.tasks) == 0
    pet.add_task(Task("Dinner", "18:00"))
    assert len(pet.tasks) == 1
