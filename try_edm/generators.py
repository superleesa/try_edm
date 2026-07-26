from __future__ import annotations

import random

from try_edm.defaults import DEFAULT_BPM, DEFAULT_INSTRUMENT, DEFAULT_VELOCITY
from try_edm.models import PatternModel


def random_pattern() -> PatternModel:
    scale = ["C4", "D#4", "F4", "G4", "A#4", "C5"]
    durations = [8, 8, 8, 16, 16, 4]
    notes = []

    for _ in range(8):
        note_name = random.choice(scale)
        duration = random.choice(durations)
        notes.append(f"{note_name}/{duration}")

    return PatternModel(
        name="random-idea",
        instrument=DEFAULT_INSTRUMENT,
        velocity=DEFAULT_VELOCITY,
        bpm=DEFAULT_BPM,
        notes=notes,
    )
