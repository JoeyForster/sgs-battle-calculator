# SGS Battle Calculator

A local FastAPI web app for resolving SGS tabletop battles without doing the battle math by hand.

The app is designed as a play aid, not a full game automation layer. You manually set up the current turn, sides, units, terrain, cards/modifiers, and seed in the browser. The calculator resolves the battle, previews health losses and destroyed units, then applies those losses only when you choose `End Turn / Apply Losses`.

## Quick Start

From this repository root:

```powershell
python -m pip install -e ".[dev]"
python -m uvicorn sgs_calculator.main:app --reload
```

Open the local app at:

```text
http://127.0.0.1:8000
```

If port `8000` is already being used, run:

```powershell
python -m uvicorn sgs_calculator.main:app --reload --port 8001
```

Then open `http://127.0.0.1:8001`.

## Build And Test

There is no frontend build pipeline yet; the browser UI is plain HTML, CSS, and JavaScript served by FastAPI.

Install the project:

```powershell
python -m pip install -e ".[dev]"
```

Run tests:

```powershell
python -m pytest
```

Run the local development server:

```powershell
python -m uvicorn sgs_calculator.main:app --reload
```

## Documentation

The detailed project notes live in [docs/](docs/README.md):

- [Developer setup and localhost workflow](docs/development.md)
- [UI guide for using the calculator during play](docs/ui-guide.md)
- [Battle rules theory and engine assumptions](docs/rules-theory.md)
- [JSON data model and API contract](docs/data-model.md)
- [Scenario presets and roster notes](docs/scenarios.md)

## Local API

When the server is running on localhost:

- `GET /` opens the calculator UI.
- `GET /api/example` returns starter battle JSON.
- `POST /api/validate` validates battle JSON and returns structured errors.
- `POST /api/simulate` returns a deterministic battle report for the submitted seed.

## Current Scope

Version 1 focuses on land battle resolution: unit health, combat factors, Rate of Fire, morale, terrain, cards/modifiers, battle phases, panic/rout checks, pursuit, survivors, and campaign Victory Point tracking in the browser.

Movement, supply, a complete card deck, sieges, and full map automation are intentionally outside the first version.
