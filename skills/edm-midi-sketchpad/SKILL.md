---
name: edm-midi-sketchpad
description: "Work on the try_edm MIDI sketchpad: edit YAML pattern banks and song arrangements, generate audition MIDIs, and preserve local/private music data conventions."
---

# EDM MIDI Sketchpad

Use this skill when the user is working on the `try_edm` project or asks to create, edit, organize, render, or explain its YAML-based MIDI patterns and arrangements.

## Project Shape

The project is a small Python/`uv` MIDI sketchpad using `pretty_midi`, `PyYAML`, and Pydantic.

- `data/patterns.yaml` is the reusable pattern bank.
- `data/song.yaml` is the default full arrangement.
- `data/songs/*.yaml` are one-track audition songs.
- `data/generated/*.mid` contains rendered audition MIDIs.
- `data/`, `*.mid`, `.venv/`, and `.mypy_cache/` are ignored and should generally stay local/private.
- `main.py` is the CLI entrypoint.
- `try_edm/models.py` defines the Pydantic YAML models.
- `try_edm/tokens.py` parses note tokens like `C4/8` into `MusicToken`.
- `try_edm/render.py` converts tokens into `pretty_midi.Note` objects and writes MIDI.
- `try_edm/generators.py` owns pattern generation such as `random_pattern()`.

## YAML Conventions

Pattern bank entries look like:

```yaml
patterns:
  - name: rising-lift
    instrument: 81
    velocity: 92
    bpm: 128
    notes:
      - C4/8
      - D4/8
```

Song files look like:

```yaml
bpm: 128
output: data/generated/rising-lift.mid

layers:
  - ref: rising-lift
    start: 0
    repeat: 4
```

A layer can either reference a pattern with `ref` or define `notes` inline. `start` is measured in beats. `repeat` repeats the pattern back-to-back. Note tokens use `NOTE/DURATION`; examples: `C4/8`, `G3/4`, `R/8`.

## Common Tasks

When adding reusable musical ideas, add them to `data/patterns.yaml` with stable descriptive names. If the user wants audition files, create one YAML file per pattern in `data/songs/`, with a single layer referencing that pattern and an output under `data/generated/`.

Render the default song with:

```bash
uv run main.py
```

Render a one-track audition song with:

```bash
uv run main.py --song data/songs/<name>.yaml
```

Use `uv run main.py --random` for random pattern exploration. If the user likes the result, paste the printed pattern block under `patterns:` in `data/patterns.yaml`.

## Important Behavior

GarageBand may display imported MIDI tracks as regions starting at bar 1 even when the notes inside start later. This is a DAW import visualization issue, not a playback timing bug. Do not add layer-stem export complexity unless the user explicitly wants separate MIDI files.

When changing code, keep tokenization separate from `pretty_midi.Note` creation:

- parse musical strings in `try_edm/tokens.py`
- resolve YAML and layer references before rendering
- create `pretty_midi.Note` objects only in the render phase

After edits, verify with the smallest useful command, usually:

```bash
uv run main.py
```

For schema or parser changes, also run:

```bash
uv run python -m py_compile main.py try_edm/*.py
```
