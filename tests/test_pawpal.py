"""Tests for the PawPal+ logic layer (pawpal_system.py).

Covers core behavior (Phase 2) plus the algorithmic layer (Phase 4): sorting,
filtering, recurrence, and conflict detection, along with a few edge cases.
"""

from datetime import date, timedelta

from pawpal_system import Owner, Pet, Task, Scheduler


def make_owner_with_tasks():
    """Owner with one pet whose tasks are added out of time order."""
    owner = Owner("Jordan")
    pet = Pet("Biscuit", "dog")
    pet.add_task(Task("Dinner", "18:00", frequency="daily"))
    pet.add_task(Task("Morning walk", "08:00", frequency="daily"))
    owner.add_pet(pet)
    return owner


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


def test_owner_all_tasks_spans_all_pets():
    """all_tasks() returns tasks from every pet the owner has."""
    owner = Owner("Jordan")
    dog = Pet("Biscuit", "dog")
    dog.add_task(Task("Walk", "08:00"))
    cat = Pet("Mochi", "cat")
    cat.add_task(Task("Feed", "09:00"))
    owner.add_pet(dog)
    owner.add_pet(cat)
    assert len(owner.all_tasks()) == 2


# --- Phase 4: sorting -------------------------------------------------------

def test_sort_by_time_is_chronological():
    """sort_by_time() returns tasks earliest-first regardless of insertion order."""
    scheduler = Scheduler(make_owner_with_tasks())
    times = [task.time for _pet, task in scheduler.sort_by_time()]
    assert times == ["08:00", "18:00"]


# --- Phase 4: filtering -----------------------------------------------------

def test_filter_by_status_returns_only_matching():
    """filter_by_status() splits done vs outstanding tasks."""
    owner = make_owner_with_tasks()
    scheduler = Scheduler(owner)
    owner.pets[0].tasks[0].mark_complete()  # complete "Dinner"
    outstanding = scheduler.filter_by_status(completed=False)
    done = scheduler.filter_by_status(completed=True)
    assert [t.description for _p, t in outstanding] == ["Morning walk"]
    assert [t.description for _p, t in done] == ["Dinner"]


def test_filter_by_pet_returns_only_that_pet():
    """filter_by_pet() returns tasks for the named pet only."""
    owner = make_owner_with_tasks()
    owner.add_pet(Pet("Mochi", "cat"))
    owner.pets[1].add_task(Task("Feed", "09:00"))
    scheduler = Scheduler(owner)
    assert len(scheduler.filter_by_pet("Biscuit")) == 2
    assert len(scheduler.filter_by_pet("Mochi")) == 1


# --- Phase 4: recurrence ----------------------------------------------------

def test_completing_daily_task_creates_next_day_occurrence():
    """Completing a daily task spawns a new, uncompleted task due one day later."""
    owner = make_owner_with_tasks()
    scheduler = Scheduler(owner)
    walk = owner.pets[0].tasks[1]  # "Morning walk", daily
    walk.due_date = date(2026, 1, 1)
    next_task = scheduler.mark_task_complete(walk)

    assert next_task is not None
    assert next_task.completed is False
    assert next_task.due_date == date(2026, 1, 2)
    assert next_task.time == "08:00"
    # The new occurrence is attached to the same pet.
    assert next_task in owner.pets[0].tasks


def test_completing_weekly_task_creates_next_week_occurrence():
    """A weekly task recurs seven days out."""
    task = Task("Grooming", "10:00", frequency="weekly", due_date=date(2026, 1, 1))
    nxt = task.next_occurrence()
    assert nxt.due_date == date(2026, 1, 1) + timedelta(weeks=1)


def test_once_task_has_no_next_occurrence():
    """A one-off task does not recur."""
    task = Task("Vet visit", "14:00", frequency="once")
    assert task.next_occurrence() is None


# --- Phase 4: conflict detection -------------------------------------------

def test_detect_conflicts_flags_same_time():
    """Two tasks at the same time (even across pets) produce a warning."""
    owner = Owner("Jordan")
    dog = Pet("Biscuit", "dog")
    dog.add_task(Task("Walk", "08:00"))
    cat = Pet("Mochi", "cat")
    cat.add_task(Task("Cuddle", "08:00"))
    owner.add_pet(dog)
    owner.add_pet(cat)
    warnings = Scheduler(owner).detect_conflicts()
    assert len(warnings) == 1
    assert "08:00" in warnings[0]


def test_no_conflict_when_times_differ():
    """Distinct times produce no conflict warnings."""
    scheduler = Scheduler(make_owner_with_tasks())
    assert scheduler.detect_conflicts() == []


# --- edge cases -------------------------------------------------------------

def test_pet_with_no_tasks_produces_empty_schedule():
    """An owner/pet with no tasks yields an empty task list, no error."""
    owner = Owner("Jordan")
    owner.add_pet(Pet("Biscuit", "dog"))
    scheduler = Scheduler(owner)
    assert scheduler.all_tasks() == []
    assert scheduler.sort_by_time() == []
    assert scheduler.detect_conflicts() == []
