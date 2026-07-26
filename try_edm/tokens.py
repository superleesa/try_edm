from __future__ import annotations

import re
from dataclasses import dataclass

from try_edm.defaults import PITCH_CLASSES


@dataclass(frozen=True)
class MusicToken:
    raw: str
    note_name: str | None
    pitch: int | None
    duration_beats: float

    @property
    def is_rest(self) -> bool:
        return self.note_name is None


def note_name_to_pitch(note_name: str) -> int:
    match = re.match(r"^([A-Ga-g])([#b]?)(-?\d+)$", note_name)
    if not match:
        raise ValueError(f"Invalid note name: {note_name}")

    letter, accidental, octave_text = match.groups()
    key = letter.upper() + accidental
    octave = int(octave_text)
    return 12 * (octave + 1) + PITCH_CLASSES[key]


def parse_music_token(raw_token: str) -> MusicToken:
    if "/" not in raw_token:
        raise ValueError(f"Missing duration in token: {raw_token}")

    note_name, duration_text = raw_token.split("/", 1)
    duration_beats = 4 / int(duration_text)

    if note_name.upper() in {"R", "REST"}:
        return MusicToken(
            raw=raw_token,
            note_name=None,
            pitch=None,
            duration_beats=duration_beats,
        )

    return MusicToken(
        raw=raw_token,
        note_name=note_name,
        pitch=note_name_to_pitch(note_name),
        duration_beats=duration_beats,
    )


def tokenize_notes(notes: list[str]) -> list[MusicToken]:
    return [parse_music_token(note) for note in notes]
