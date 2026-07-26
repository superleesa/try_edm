from __future__ import annotations

from pathlib import Path

import pretty_midi

from try_edm.arrangement import ResolvedLayer
from try_edm.tokens import MusicToken, tokenize_notes


def beats_to_seconds(beats: float, bpm: int) -> float:
    return beats * 60 / bpm


def token_to_note(
    token: MusicToken,
    start: float,
    bpm: int,
    velocity: int,
) -> tuple[pretty_midi.Note | None, float]:
    end = start + beats_to_seconds(token.duration_beats, bpm)

    if token.is_rest:
        return None, end

    if token.pitch is None:
        raise ValueError(f"Token `{token.raw}` has no pitch")

    return (
        pretty_midi.Note(
            velocity=velocity,
            pitch=token.pitch,
            start=start,
            end=end,
        ),
        end,
    )


def layer_duration_beats(layer: ResolvedLayer) -> float:
    return sum(token.duration_beats for token in tokenize_notes(layer.pattern.notes))


def render_layers(layers: list[ResolvedLayer], output_path: Path) -> None:
    pm = pretty_midi.PrettyMIDI()

    for layer in layers:
        pattern = layer.pattern
        tokens = tokenize_notes(pattern.notes)
        instrument = pretty_midi.Instrument(
            program=pattern.instrument,
            name=pattern.name,
        )
        pattern_duration = sum(token.duration_beats for token in tokens)

        for repeat_index in range(layer.repeat):
            current_time = beats_to_seconds(
                layer.start + repeat_index * pattern_duration,
                pattern.bpm,
            )
            for token in tokens:
                note, current_time = token_to_note(
                    token=token,
                    start=current_time,
                    bpm=pattern.bpm,
                    velocity=pattern.velocity,
                )
                if note is not None:
                    instrument.notes.append(note)

        pm.instruments.append(instrument)

    pm.write(str(output_path))
