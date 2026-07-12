# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Running the CLI demo (`python main.py`) produces:

```
Owner: Jordan — 2 pets

Today's Schedule:
  08:00  Morning walk (Biscuit) [daily] [todo]
  18:00  Dinner (Biscuit) [daily] [todo]
  09:30  Refill water (Mochi) [daily] [todo]
```

## 🧪 Testing PawPal+

Run the suite from the project root:

```bash
python -m pytest
```

The tests in `tests/test_pawpal.py` cover:

- **Core behavior** — `mark_complete()` flips status; adding a task grows a pet's
  task list; `Owner.all_tasks()` spans every pet.
- **Sorting** — `sort_by_time()` returns tasks chronologically regardless of insertion order.
- **Filtering** — by pet name and by completion status.
- **Recurrence** — completing a daily task creates a next-day occurrence attached to the
  same pet; weekly recurs 7 days out; one-off tasks do not recur.
- **Conflict detection** — two tasks at the same time (even across pets) produce a warning; distinct times do not.
- **Edge cases** — a pet with no tasks yields an empty, error-free schedule.

Sample run:

```
============================= test session starts ==============================
platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0
configfile: pytest.ini
testpaths: tests
collected 12 items

tests/test_pawpal.py ............                                        [100%]

============================== 12 passed in 0.02s ==============================
```

**Confidence level: ★★★★☆ (4/5).** The core logic, sorting, filtering, recurrence, and
exact-time conflict detection are all exercised by passing tests. Docking one star
because conflict detection only checks exact time matches (not overlapping durations),
which is an accepted tradeoff documented in `reflection.md`.

## 📐 Smarter Scheduling

The `Scheduler` in `pawpal_system.py` adds four algorithmic features on top of the
core data model:

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts all (pet, task) pairs chronologically. Times are zero-padded `HH:MM`, so a string sort is already chronological. |
| Filtering | `Scheduler.filter_by_pet(name)`, `Scheduler.filter_by_status(completed)` | Narrow the task list to a single pet, or to done / outstanding tasks. |
| Conflict detection | `Scheduler.detect_conflicts()` | Groups tasks by exact time and returns a warning string for any slot with 2+ tasks (returns messages, never raises). |
| Recurring tasks | `Task.next_occurrence()`, `Scheduler.mark_task_complete(task)` | Completing a `daily`/`weekly` task spawns the next occurrence via `timedelta` and attaches it to the same pet. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->


