# SGS Battle Calculator Docs

This directory is the project manual for the SGS Battle Calculator.

The calculator is built to augment live tabletop play. You still make the game decisions at the table: which battle is happening, which units are present, what terrain applies, which cards/modifiers are active, and when losses are committed. The app handles the arithmetic-heavy battle resolution and keeps the turn state tidy between battles.

## Docs Map

- [Development](development.md): install, run, localhost, tests, and troubleshooting.
- [UI Guide](ui-guide.md): how to use the browser app during a game.
- [Rules Theory](rules-theory.md): the battle-engine model, combat flow, morale theory, and assumptions.
- [Data Model](data-model.md): battle JSON structure, API endpoints, units, sides, modifiers, and tags.
- [Scenario Presets](scenarios.md): included preset scenarios and what the preset data is meant to represent.

## Project Shape

- `sgs_calculator/main.py` serves the FastAPI app and JSON endpoints.
- `sgs_calculator/models.py` defines the Pydantic request/response schema.
- `sgs_calculator/engine.py` contains the pure Python deterministic battle engine.
- `sgs_calculator/static/` contains the browser UI.
- `tests/` contains engine and API tests.

## Design Intent

The app is a calculator first:

- Manual input stays visible and editable.
- Full names are shown in the UI instead of requiring players to remember stat acronyms.
- Dark mode is available and defaults on.
- Health bars show current unit strength.
- Dead units are previewed after a battle and removed only when losses are applied.
- Scenario presets help start common SGS battles faster, but everything remains editable.
