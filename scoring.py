"""Simple wellness score (0–100) and one primary recommendation."""

from __future__ import annotations

from typing import Any


def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def score_profile(profile: dict[str, Any]) -> tuple[int, str, dict[str, float]]:
    """
    Returns (score 0-100, one recommendation, component scores for UI).
    """
    age = int(profile.get("age") or 30)
    sleep = float(profile.get("sleep_hours") or 7.0)
    habits = profile.get("habits") or {}
    water = int(habits.get("water_glasses") or 0)
    exercise = int(habits.get("exercise_minutes") or 0)
    steps = int(habits.get("steps_per_day") or 0)

    # Sleep: peak around 7–9h
    if 7 <= sleep <= 9:
        sleep_pts = 100.0
    elif sleep < 7:
        sleep_pts = _clamp(40 + (sleep / 7) * 55, 0, 99)
    else:
        sleep_pts = _clamp(100 - (sleep - 9) * 12, 55, 100)

    # Water: target ~8 glasses
    water_pts = _clamp((water / 8) * 100, 0, 100)

    # Exercise: target ~30 min
    exercise_pts = _clamp((exercise / 30) * 100, 0, 100)

    # Steps: target ~8000
    steps_pts = _clamp((steps / 8000) * 100, 0, 100)

    # Age: tiny nudge only for demo transparency (optional)
    _ = age  # reserved for future personalization

    weights = {"sleep": 0.35, "water": 0.2, "exercise": 0.25, "steps": 0.2}
    total = (
        sleep_pts * weights["sleep"]
        + water_pts * weights["water"]
        + exercise_pts * weights["exercise"]
        + steps_pts * weights["steps"]
    )
    score = int(round(_clamp(total, 0, 100)))

    components = {
        "sleep": round(sleep_pts, 1),
        "water": round(water_pts, 1),
        "exercise": round(exercise_pts, 1),
        "steps": round(steps_pts, 1),
    }

    # One recommendation: weakest weighted gap
    gaps = {
        "sleep": (100 - sleep_pts) * weights["sleep"],
        "hydration": (100 - water_pts) * weights["water"],
        "exercise": (100 - exercise_pts) * weights["exercise"],
        "daily movement": (100 - steps_pts) * weights["steps"],
    }
    worst = max(gaps, key=gaps.get)

    if worst == "sleep":
        rec = "Prioritize a consistent sleep window (aim for 7–9 hours) and wind down screens 30–60 minutes before bed."
    elif worst == "hydration":
        rec = "Increase hydration gradually: add 1 extra glass of water today and tie it to an existing habit (meals or breaks)."
    elif worst == "exercise":
        rec = "Add a small movement block you can repeat daily (10–20 minutes of brisk walking or bodyweight work)."
    else:
        rec = "Boost daily movement with short walks after meals or a parking-lap routine to push steps closer to your goal."

    return score, rec, components
