# PawPal+ Project Reflection

### Core user actions

Three things a PawPal+ user should be able to do:

1. **Add a pet** (name + species) that they want to care for.
2. **Schedule a care task** for a pet — a description, a time of day, and how often it
   repeats (once / daily / weekly).
3. **See today's schedule** — all tasks across all pets, sorted by time, with any
   scheduling conflicts flagged.

## 1. System Design

**a. Initial design**

My initial UML (`diagrams/uml_draft.mmd`) has four classes:

- **Task** — one care activity. Holds a `description`, a `time` ("HH:MM"), a
  `frequency` ("once"/"daily"/"weekly"), a `completed` flag, and a `due_date`. It can
  `mark_complete()` itself and produce its `next_occurrence()` when recurring.
- **Pet** — a `name`, `species`, and its own `tasks` list. It can `add_task()`.
- **Owner** — a `name` and a list of `pets`. It can `add_pet()` and gather `all_tasks()`
  across every pet.
- **Scheduler** — the "brain". It reads the owner's pets/tasks and provides the smart
  behavior: sort by time, filter by pet or status, mark tasks complete (spawning the
  next recurrence), and detect time conflicts.

Responsibility split: the data classes (`Task`, `Pet`, `Owner`) just hold state and do
minimal self-management; the `Scheduler` owns all cross-pet logic so the algorithms live
in one place.

**b. Design changes**

Yes. The biggest change was replacing an earlier "time-budget planner" design (where the
owner had a fixed number of available minutes and tasks were packed by priority) with the
current **multi-pet task manager**. The budget model didn't fit the real scenario — a pet
owner thinks in terms of "which pet, what task, at what time," not "how many minutes do I
have." Restructuring so `Owner` owns `Pet`s and each `Pet` owns its `Task`s made the
relationships natural and unlocked per-pet filtering and cross-pet conflict detection.

A smaller change: I moved recurrence so that `Task.next_occurrence()` builds the new task
but `Scheduler.mark_task_complete()` is what attaches it to the right pet. That kept `Task`
free of any knowledge about pets while still making completion "automatically" schedule the
next occurrence.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers **time of day** (to order the plan and to detect conflicts) and
**completion status** and **pet ownership** (to filter). Time mattered most because a daily
plan is fundamentally "what happens when," and the most useful safety check for an owner is
"have I accidentally booked two things at once." I deliberately left out a duration/priority
constraint to keep the model a set of point-in-time events rather than intervals — simpler,
and enough for the core scenario.

**b. Tradeoffs**

`Scheduler.detect_conflicts()` only flags tasks that share the **exact same start
time** ("HH:MM"). It does not consider task duration or overlapping windows — two
tasks at 08:00 and 08:15 are treated as non-conflicting even if the first "takes"
30 minutes.

This is reasonable for PawPal+ because the model has no duration field: tasks are
points in time, not intervals. Exact-match detection is simple, fast, and predictable,
and it catches the most common real mistake (double-booking the same slot). Adding
true overlap detection would require a duration attribute and interval math — worth it
later, but unnecessary complexity for the current point-in-time model.

---

## 3. AI Collaboration

**a. How you used AI**

I used my AI coding assistant across the whole workflow: brainstorming the class
breakdown, generating the Mermaid UML, scaffolding dataclass skeletons, implementing the
algorithmic methods, and drafting the test suite. The most helpful prompts were **specific
and grounded in my files** — e.g. "based on my skeletons, how should the Scheduler retrieve
all tasks from the Owner's pets?" and "give me a lightweight conflict-detection strategy
that returns a warning instead of crashing." Open-ended prompts produced generic code;
prompts referencing my actual class names produced code I could drop in.

**b. Judgment and verification**

I rejected the original **time-budget scheduler** design even though it was clean and fully
tested, because it didn't match how a pet owner actually plans a day. That was a
human-architecture call the AI wouldn't make on its own. I verified every AI suggestion by
running `python main.py` (to eyeball real behavior) and `python -m pytest` (to confirm the
contracts held) — for example, I only trusted the recurrence logic once a test showed the
next occurrence was uncompleted, dated one day later, and attached to the same pet.

### AI Strategy (Phase 6)

- **Most effective features:** inline chat grounded in attached files (for targeted method
  implementations) and agent-style multi-file edits (for the recurrence change that touched
  both `Task` and `Scheduler`).
- **A suggestion I modified:** an early version put recurrence entirely inside `Task`, which
  forced `Task` to know about pets. I moved the "attach the next occurrence" step up into
  `Scheduler.mark_task_complete()` to keep the data classes ignorant of ownership.
- **Separate chat sessions per phase** kept design discussion from bleeding into testing
  discussion — the testing chat stayed focused on edge cases instead of re-litigating the
  data model.
- **Lead-architect takeaway:** the AI is fastest at producing plausible code, but I had to
  own the decisions about *what* to build and *why*. My job was choosing the design,
  verifying behavior, and rejecting suggestions that were clean but wrong for the scenario.

---

## 4. Testing and Verification

**a. What you tested**

Twelve tests in `tests/test_pawpal.py` cover: marking tasks complete, adding tasks to
pets, `Owner.all_tasks()` spanning multiple pets, chronological sorting, filtering by pet
and by status, daily/weekly recurrence (and that one-off tasks don't recur), conflict
detection on same-time tasks, and an empty-schedule edge case. These matter because they
lock in the exact behaviors the UI and CLI depend on — especially recurrence and conflict
detection, which have the most moving parts.

**b. Confidence**

Fairly confident (4/5) — every core behavior and algorithm is covered by a passing test,
and the CLI demo exercises them end-to-end. With more time I'd test overlapping-duration
conflicts (once a duration field exists), tasks spanning midnight, and invalid time strings
like "8am" or "" to make parsing robust.

---

## 5. Reflection

**a. What went well**

The clean separation between the data classes and the `Scheduler` "brain." Because all the
logic lives in one place, both the CLI (`main.py`) and the Streamlit UI (`app.py`) share the
exact same behavior with no duplicated logic — the UI is genuinely just a thin presentation
layer.

**b. What you would improve**

I'd add a `duration` to `Task` and upgrade conflict detection from exact-time matching to
true interval overlap, plus data persistence (save/load to JSON) so pets and tasks survive
between runs. I'd also validate the `HH:MM` time input at the boundary instead of trusting it.

**c. Key takeaway**

Designing the relationships first (Owner → Pet → Task) made everything downstream easier —
sorting, filtering, and conflict detection all fell out naturally once the data model was
right. And working with AI, the leverage came from being a decisive architect: the AI writes
code quickly, but the quality of the result depended on me choosing the right design and
verifying behavior rather than accepting the first plausible answer.
