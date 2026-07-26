from __future__ import annotations

from pathlib import Path
from typing import Any

from pydantic import AliasChoices, BaseModel, ConfigDict, Field, field_validator, model_validator

from try_edm.defaults import DEFAULT_BPM, DEFAULT_INSTRUMENT, DEFAULT_VELOCITY


def normalize_notes(value: Any) -> list[str]:
    if isinstance(value, str):
        return value.split()
    if isinstance(value, list):
        return [str(note) for note in value]
    return []


class PatternModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    instrument: int = DEFAULT_INSTRUMENT
    velocity: int = DEFAULT_VELOCITY
    bpm: int = DEFAULT_BPM
    notes: list[str]

    @field_validator("notes", mode="before")
    @classmethod
    def coerce_notes(cls, value: Any) -> list[str]:
        return normalize_notes(value)

    @model_validator(mode="after")
    def require_notes(self) -> PatternModel:
        if not self.notes:
            raise ValueError(f"Pattern `{self.name}` is missing notes")
        return self


class PatternBankModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    patterns: list[PatternModel] = Field(default_factory=list)

    @model_validator(mode="after")
    def require_unique_pattern_names(self) -> PatternBankModel:
        seen = set()
        for pattern in self.patterns:
            if pattern.name in seen:
                raise ValueError(f"Duplicate pattern name: {pattern.name}")
            seen.add(pattern.name)
        return self


class LayerModel(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    ref: str | None = None
    pattern: str | None = None
    name: str | None = None
    instrument: int | None = None
    velocity: int | None = None
    bpm: int | None = None
    notes: list[str] | None = None
    start: float = Field(default=0, validation_alias=AliasChoices("start", "at"))
    repeat: int = 1

    @field_validator("notes", mode="before")
    @classmethod
    def coerce_notes(cls, value: Any) -> list[str]:
        return normalize_notes(value)

    @model_validator(mode="after")
    def require_ref_or_notes(self) -> LayerModel:
        if not self.ref and not self.pattern and not self.notes:
            raise ValueError("Layer must define `ref` or `notes`")
        return self


class SongModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    bpm: int = DEFAULT_BPM
    output: Path = Path("song.mid")
    layers: list[LayerModel] = Field(default_factory=list)

    @model_validator(mode="after")
    def require_layers(self) -> SongModel:
        if not self.layers:
            raise ValueError("Song has no layers")
        return self
