# try-edm

A tiny MIDI sketchpad for experimenting with simple EDM ideas.

The project uses two YAML files in `data/`:

- `data/patterns.yaml`: your private bank of reusable pattern ideas.
- `data/song.yaml`: the actual arrangement that decides which patterns play, when they start, and which layers play together.

`data/` is gitignored so you can freely collect rough ideas without committing them.

## Setup

Install and sync dependencies with `uv`:

```bash
uv sync
```

## Render The Song

Generate `song.mid` from `data/song.yaml`:

```bash
uv run main.py
```

You can override the input files:

```bash
uv run main.py --patterns data/patterns.yaml --song data/song.yaml
```

Or override the output file:

```bash
uv run main.py --output my-song.mid
```

## Try Random Patterns

Generate a random idea into `random.mid`:

```bash
uv run main.py --random
```

The command also prints a YAML block. If you like the sound, paste that block under `patterns:` in `data/patterns.yaml`.

## Pattern Bank Format

Example `data/patterns.yaml`:

```yaml
patterns:
  - name: first-saw-lead
    instrument: 81
    velocity: 100
    bpm: 128
    notes:
      - C4/8
      - E4/8
      - G4/8
      - C5/4
```

Notes use this format:

```text
NOTE/DURATION
```

Examples:

- `C4/8`: C4 eighth note
- `G3/4`: G3 quarter note
- `R/8`: eighth-note rest

## Song Arrangement Format

Example `data/song.yaml`:

```yaml
bpm: 128
output: song.mid

layers:
  - ref: first-saw-lead
    start: 0

  - name: direct-low-saw
    instrument: 81
    velocity: 75
    start: 0
    repeat: 2
    notes:
      - C3/4
      - R/8
      - G3/8
```

A layer can either:

- reference a bank pattern with `ref`
- define notes directly with `notes`

`start` is measured in beats. Layers with the same `start` play together.

## Code Layout

```text
try_edm/
  defaults.py      default BPM, instrument, velocity, and pitch classes
  models.py        Pydantic models for YAML parsing
  yaml_io.py       YAML file loading
  arrangement.py   resolve refs and inline layers
  tokens.py        convert strings like C4/8 into MusicToken objects
  render.py        convert MusicToken objects into pretty_midi.Note objects
  generators.py    random pattern generation
```
