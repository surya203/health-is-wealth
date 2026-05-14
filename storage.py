"""Load and save wellness data as JSON in the project root."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


DATA_FILE = Path(__file__).resolve().parent / "wellness_data.json"


def default_data() -> dict[str, Any]:
    return {
        "profile": {
            "age": 30,
            "sleep_hours": 7.0,
            "habits": {
                "water_glasses": 5,
                "exercise_minutes": 15,
                "steps_per_day": 6000,
            },
        },
        "chat_history": [],
    }


def load_data() -> dict[str, Any]:
    if not DATA_FILE.exists():
        return default_data()
    with DATA_FILE.open(encoding="utf-8") as f:
        raw = json.load(f)
    # Merge with defaults for any new keys
    base = default_data()
    if isinstance(raw.get("profile"), dict):
        base["profile"].update(raw["profile"])
        if isinstance(raw["profile"].get("habits"), dict):
            base["profile"]["habits"].update(raw["profile"]["habits"])
    if isinstance(raw.get("chat_history"), list):
        base["chat_history"] = raw["chat_history"][-50:]
    return base


def save_data(data: dict[str, Any]) -> None:
    data["chat_history"] = data.get("chat_history", [])[-50:]
    tmp = DATA_FILE.with_suffix(".tmp")
    text = json.dumps(data, indent=2, ensure_ascii=False)
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(DATA_FILE)
