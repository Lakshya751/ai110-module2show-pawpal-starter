"""PawPal+ CLI demo.

A standalone "testing ground" that exercises the logic layer in the terminal,
independent of the Streamlit UI. Run with: python main.py
"""

from pawpal_system import Owner, Pet, Task, Scheduler


def build_demo_owner() -> Owner:
    """Create an owner with two pets and tasks added out of time order."""
    owner = Owner(name="Jordan")

    biscuit = Pet(name="Biscuit", species="dog")
    # Added out of order on purpose to show sort_by_time() at work.
    biscuit.add_task(Task("Dinner", "18:00", frequency="daily"))
    biscuit.add_task(Task("Morning walk", "08:00", frequency="daily"))

    mochi = Pet(name="Mochi", species="cat")
    mochi.add_task(Task("Refill water", "09:30", frequency="daily"))
    # Same time as Biscuit's walk -> should trigger a conflict warning.
    mochi.add_task(Task("Morning cuddle", "08:00", frequency="weekly"))

    owner.add_pet(biscuit)
    owner.add_pet(mochi)
    return owner


def main() -> None:
    owner = build_demo_owner()
    scheduler = Scheduler(owner)

    print(f"Owner: {owner.name} — {len(owner.pets)} pets\n")

    # Sorted schedule + conflict detection.
    print(scheduler.todays_schedule())

    # Filtering: only Biscuit's tasks.
    print("\nBiscuit's tasks only:")
    for pet, task in scheduler.filter_by_pet("Biscuit"):
        print(f"  {task.time}  {task.description}")

    # Recurring: completing a daily task spawns tomorrow's occurrence.
    walk = owner.pets[0].tasks[1]  # Biscuit's "Morning walk" (daily)
    next_walk = scheduler.mark_task_complete(walk)
    print("\nAfter completing Biscuit's daily 'Morning walk':")
    print(f"  completed flag: {walk.completed}")
    print(f"  next occurrence due: {next_walk.due_date} at {next_walk.time}")

    # Filtering: what's still outstanding.
    print("\nOutstanding (not completed) tasks:")
    for pet, task in scheduler.filter_by_status(completed=False):
        print(f"  {task.time}  {task.description} ({pet.name})")


if __name__ == "__main__":
    main()
