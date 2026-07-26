from __future__ import annotations

import argparse
from pathlib import Path

from try_edm.arrangement import ResolvedLayer, resolve_layers
from try_edm.generators import random_pattern
from try_edm.models import PatternModel
from try_edm.render import render_layers
from try_edm.yaml_io import load_pattern_bank, load_song


def pattern_to_bank_yaml(pattern: PatternModel) -> str:
    lines = [
        f"  - name: {pattern.name}",
        f"    instrument: {pattern.instrument}",
        f"    velocity: {pattern.velocity}",
        f"    bpm: {pattern.bpm}",
        "    notes:",
    ]
    lines.extend(f"      - {note}" for note in pattern.notes)
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--patterns", default="data/patterns.yaml")
    parser.add_argument("--song", default="data/song.yaml")
    parser.add_argument("--output")
    parser.add_argument("--random", action="store_true")
    args = parser.parse_args()

    if args.random:
        pattern = random_pattern()
        render_layers([ResolvedLayer(pattern=pattern, start=0, repeat=1)], Path("random.mid"))
        print(pattern_to_bank_yaml(pattern))
        print("\nWrote random.mid. If you like it, paste the block above into data/patterns.yaml under `patterns:`.")
        return

    bank = load_pattern_bank(Path(args.patterns))
    song = load_song(Path(args.song))
    layers = resolve_layers(song, bank)
    output_path = Path(args.output) if args.output else song.output
    render_layers(layers, output_path)
    print(f"Wrote {output_path} from {len(layers)} layer(s).")


if __name__ == "__main__":
    main()
