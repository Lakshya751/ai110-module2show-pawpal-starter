"""PawPal+ Streamlit UI.

Thin presentation layer over the logic in pawpal_system.py. All pet/task/schedule
state lives in a single Owner object stored in st.session_state so it survives
Streamlit's top-to-bottom reruns.
"""

import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption("A pet-care planner: add pets, schedule tasks, and see today's plan.")

# --- Application memory -----------------------------------------------------
# Streamlit reruns this script on every interaction. Store the Owner once so
# pets and tasks persist across reruns instead of being rebuilt empty.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")

owner: Owner = st.session_state.owner

# --- Owner ------------------------------------------------------------------
owner.name = st.text_input("Owner name", value=owner.name)

st.divider()

# --- Add a pet --------------------------------------------------------------
st.subheader("🐶 Add a pet")
with st.form("add_pet", clear_on_submit=True):
    pet_name = st.text_input("Pet name", value="")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    if st.form_submit_button("Add pet"):
        if pet_name.strip():
            owner.add_pet(Pet(name=pet_name.strip(), species=species))
            st.success(f"Added {pet_name.strip()} ({species}).")
        else:
            st.warning("Please enter a pet name.")

if owner.pets:
    st.caption("Current pets: " + ", ".join(f"{p.name} ({p.species})" for p in owner.pets))
else:
    st.info("No pets yet. Add one above.")

st.divider()

# --- Add a task -------------------------------------------------------------
st.subheader("📝 Schedule a task")
if not owner.pets:
    st.info("Add a pet first, then you can schedule tasks for it.")
else:
    with st.form("add_task", clear_on_submit=True):
        pet_choice = st.selectbox("Pet", [p.name for p in owner.pets])
        description = st.text_input("Task description", value="Morning walk")
        time = st.text_input("Time (HH:MM)", value="08:00")
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
        if st.form_submit_button("Add task"):
            pet = next(p for p in owner.pets if p.name == pet_choice)
            pet.add_task(Task(description=description, time=time, frequency=frequency))
            st.success(f"Scheduled '{description}' at {time} for {pet_choice}.")

st.divider()

# --- Today's schedule -------------------------------------------------------
st.subheader("🗓️ Today's schedule")
scheduler = Scheduler(owner)

# Conflict warnings surface at the top so the owner sees double-bookings first.
for warning in scheduler.detect_conflicts():
    st.warning(f"⚠️ {warning}")

# Filters use the Scheduler's methods; default view is time-sorted.
col_a, col_b = st.columns(2)
with col_a:
    pet_filter = st.selectbox("Filter by pet", ["All pets"] + [p.name for p in owner.pets])
with col_b:
    status_filter = st.selectbox("Filter by status", ["All", "Outstanding", "Done"])

pairs = scheduler.sort_by_time()
if pet_filter != "All pets":
    pairs = [pr for pr in pairs if pr[0].name == pet_filter]
if status_filter == "Outstanding":
    pairs = [pr for pr in pairs if not pr[1].completed]
elif status_filter == "Done":
    pairs = [pr for pr in pairs if pr[1].completed]

if pairs:
    st.table(
        [
            {
                "Time": task.time,
                "Task": task.description,
                "Pet": pet.name,
                "Frequency": task.frequency,
                "Status": "✅ done" if task.completed else "⏳ todo",
            }
            for pet, task in pairs
        ]
    )
else:
    st.info("No tasks match the current filters.")
