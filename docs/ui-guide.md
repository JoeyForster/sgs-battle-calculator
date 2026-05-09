# UI Guide

## Intended Workflow

1. Choose or load a scenario preset.
2. Adjust the scenario name, turn number, target Victory Points, side names, and battle name.
3. Add or edit units in the Unit Library.
4. Stage units into the attacker and defender battlefield stacks.
5. Select terrain and active cards/modifiers.
6. Press `Start Battle`.
7. Review the battle result, round timeline, dice rolls, and health previews.
8. Press `End Turn / Apply Losses` when you are ready to commit the result.

## Scenario Presets

The preset selector loads a scenario roster, side names, starting battle name, terrain, seed, and starting stacks. Presets are only a starting point. After loading one, you can change any value before resolving the battle.

## Unit Library

The Unit Library is the roster pool for the current game state.

Each unit has:

- Side assignment.
- Unit name and country.
- Domain: land or air.
- Role: combat or support.
- Unit type.
- Current Health and Maximum Health.
- Stacking Value.
- Attack Factor, Defense Factor, Morale Factor, and Rate of Fire.
- Traits such as Elite, Pursuer, Breakthrough, and Recon.

Use the attacker/defender buttons on a unit card to stage it into the current battle.

Country flags, unit type icons, and trait icons appear on unit cards when the country/type/trait is recognized. Custom countries fall back to a readable two-letter marker.

## Health Bars

Health bars show `Current Health / Maximum Health`.

After `Start Battle`, the battlefield cards switch to a projected survivor preview:

- Destroyed units show `0 / max` and a destroyed status badge.
- Damaged units show their reduced health.
- Panicked units show a panicked status badge.

The library is not permanently changed until `End Turn / Apply Losses` is pressed.

## Battlefield

The center of the page holds the current battle:

- Attacker and defender side names update dynamically.
- Battle Morale previews update as staged units, terrain, and morale cards change.
- `Max Battle Phases` controls how many post-main battle phases can happen.
- `Defender entrenched` adds the engine's entrenchment penalty against the attacker.
- `Province size` is used as the defender connection modifier in the first combat round.

## Terrain, Cards, And Glossary

The right panel has three tabs:

- `Terrain`: search and select the active terrain preset.
- `Cards`: apply generic battle modifiers to attacker or defender.
- `Glossary`: search full stat and trait names used by the calculator.

The main UI intentionally shows full labels such as `Attack Factor`, `Defense Factor`, `Morale Factor`, `Rate of Fire`, and `Battle Morale` instead of relying on acronyms.

## Dark Mode

Dark mode is available from the top-right theme button. The choice is saved in the browser's local storage.

## JSON Export

`View JSON` shows the generated battle payload. This is useful for debugging validation errors, saving a battle setup, or writing tests.

The JSON is the contract between the browser and the Python engine. Details are documented in [Data Model](data-model.md).
