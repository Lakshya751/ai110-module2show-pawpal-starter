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

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
