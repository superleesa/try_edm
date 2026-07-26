from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from try_edm.models import PatternBankModel, PatternModel, SongModel


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text())
    return data if data else {}


def load_pattern_bank(path: Path) -> dict[str, PatternModel]:
    bank = PatternBankModel.model_validate(load_yaml(path))
    return {pattern.name: pattern for pattern in bank.patterns}


def load_song(path: Path) -> SongModel:
    return SongModel.model_validate(load_yaml(path))
