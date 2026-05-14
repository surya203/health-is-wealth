"""
Wellness demo: profile → score + recommendation → rule-based chat.
Run: streamlit run app.py
"""

from __future__ import annotations

import streamlit as st

from coach import coach_reply
from scoring import score_profile
from storage import load_data, save_data, default_data

st.set_page_config(page_title="Wellness Coach Demo", page_icon="🌿", layout="centered")

st.title("🌿 Wellness Coach")
st.caption("Profile → wellness score → one recommendation → coaching chat.")

data = load_data()
profile = data["profile"]
habits = profile.setdefault("habits", {})

with st.sidebar:
    st.header("Your profile")
    age = st.number_input("Age", min_value=13, max_value=120, value=int(profile.get("age", 30)))
    sleep_hours = st.slider(
        "Average sleep (hours/night)",
        min_value=4.0,
        max_value=12.0,
        step=0.5,
        value=float(profile.get("sleep_hours", 7.0)),
    )
    st.subheader("Habits (approximate)")
    water_glasses = st.slider("Water (glasses/day)", 0, 14, int(habits.get("water_glasses", 5)))
    exercise_minutes = st.slider("Exercise (minutes/day)", 0, 120, int(habits.get("exercise_minutes", 15)))
    steps_per_day = st.slider("Steps (per day)", 0, 20000, int(habits.get("steps_per_day", 6000)), step=500)

    if st.button("Save profile", type="primary"):
        data["profile"] = {
            "age": age,
            "sleep_hours": sleep_hours,
            "habits": {
                "water_glasses": water_glasses,
                "exercise_minutes": exercise_minutes,
                "steps_per_day": steps_per_day,
            },
        }
        save_data(data)
        st.success("Saved to wellness_data database")

profile_for_score = {
    "age": age,
    "sleep_hours": sleep_hours,
    "habits": {
        "water_glasses": water_glasses,
        "exercise_minutes": exercise_minutes,
        "steps_per_day": steps_per_day,
    },
}

score, recommendation, components = score_profile(profile_for_score)

col1, col2 = st.columns(2)
with col1:
    st.metric("Wellness score", f"{score} / 100")
with col2:
    st.caption("Weighted mix of sleep, hydration, exercise, and steps.")

with st.expander("How this score breaks down"):
    st.write(
        {
            "Sleep quality (vs 7–9h)": components["sleep"],
            "Hydration (vs ~8 glasses)": components["water"],
            "Exercise (vs ~30 min)": components["exercise"],
            "Movement (vs ~8000 steps)": components["steps"],
        }
    )

st.subheader("Today’s top recommendation")
st.info(recommendation)

st.divider()
st.subheader("Coaching chat")

for msg in data.get("chat_history", []):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Ask about sleep, stress, water, exercise, motivation…")
if prompt:
    data.setdefault("chat_history", []).append({"role": "user", "content": prompt})
    reply = coach_reply(prompt)
    data["chat_history"].append({"role": "assistant", "content": reply})
    save_data(data)
    st.rerun()
