from __future__ import annotations

from dataclasses import dataclass

from try_edm.defaults import DEFAULT_INSTRUMENT, DEFAULT_VELOCITY
from try_edm.models import LayerModel, PatternModel, SongModel


@dataclass(frozen=True)
class ResolvedLayer:
    pattern: PatternModel
    start: float
    repeat: int


def resolve_pattern(base: PatternModel, layer: LayerModel, song_bpm: int) -> PatternModel:
    return PatternModel(
        name=layer.name or base.name,
        instrument=layer.instrument if layer.instrument is not None else base.instrument,
        velocity=layer.velocity if layer.velocity is not None else base.velocity,
        bpm=layer.bpm if layer.bpm is not None else song_bpm,
        notes=layer.notes or base.notes,
    )


def inline_pattern(layer: LayerModel, song_bpm: int, index: int) -> PatternModel:
    return PatternModel(
        name=layer.name or f"layer-{index}",
        instrument=layer.instrument if layer.instrument is not None else DEFAULT_INSTRUMENT,
        velocity=layer.velocity if layer.velocity is not None else DEFAULT_VELOCITY,
        bpm=layer.bpm if layer.bpm is not None else song_bpm,
        notes=layer.notes or [],
    )


def resolve_layers(song: SongModel, bank: dict[str, PatternModel]) -> list[ResolvedLayer]:
    layers = []

    for index, layer in enumerate(song.layers, start=1):
        ref_name = layer.ref or layer.pattern
        if ref_name:
            if ref_name not in bank:
                raise ValueError(f"Layer {index} references unknown pattern `{ref_name}`")
            pattern = resolve_pattern(bank[ref_name], layer, song.bpm)
        else:
            pattern = inline_pattern(layer, song.bpm, index)

        layers.append(
            ResolvedLayer(
                pattern=pattern,
                start=layer.start,
                repeat=layer.repeat,
            )
        )

    return layers
