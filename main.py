"""PawPal+ CLI demo.

A standalone "testing ground" that exercises the logic layer in the terminal,
independent of the Streamlit UI. Run with: python main.py
"""

from pawpal_system import Owner, Pet, Task


def build_demo_owner() -> Owner:
    """Create an owner with two pets and a few tasks for the demo."""
    owner = Owner(name="Jordan")

    biscuit = Pet(name="Biscuit", species="dog")
    biscuit.add_task(Task("Morning walk", "08:00", frequency="daily"))
    biscuit.add_task(Task("Dinner", "18:00", frequency="daily"))

    mochi = Pet(name="Mochi", species="cat")
    mochi.add_task(Task("Refill water", "09:30", frequency="daily"))

    owner.add_pet(biscuit)
    owner.add_pet(mochi)
    return owner


def main() -> None:
    from pawpal_system import Scheduler

    owner = build_demo_owner()
    scheduler = Scheduler(owner)

    print(f"Owner: {owner.name} — {len(owner.pets)} pets\n")
    print(scheduler.todays_schedule())


if __name__ == "__main__":
    main()
