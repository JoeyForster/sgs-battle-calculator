# Scenario Presets

Scenario presets are editable starter states for the browser UI. They are intended to make setup faster, not to lock the player into a fixed roster.

Loading a preset updates:

- Scenario name.
- Attacker and defender side names.
- Battle name.
- Seed.
- Terrain.
- Unit library.
- Initial attacker and defender stacks.

## Included Presets

| Preset | Attacker | Defender | Starting Battle |
| --- | --- | --- | --- |
| SGS Afrika Korps | Axis | Commonwealth | Sidi Barrani |
| SGS Afrika Korps: Tunisia | Axis | Allies | Kasserine Pass |
| SGS Winter War | Soviet Union | Finland | Karelian Isthmus |
| SGS Halls of Montezuma | United States | Mexico | Chapultepec |
| SGS Heia Safari | German East Africa | British Empire | East African Campaign |
| SGS Operation Hawaii | Imperial Japan | United States | Oahu |

## Preset Theory

The current presets provide plausible battle stacks and unit traits for testing and play-aid setup. They are not yet a complete counter-by-counter transcription of every SGS game.

Use presets as a fast starting point:

- Add missing units from the Unit Library form.
- Adjust Current Health after previous battles.
- Change terrain if the battle location differs.
- Add cards/modifiers for the actual situation.
- Save the browser state before resolving a major turn.

## Adding More Presets

Preset data currently lives in `sgs_calculator/static/app.js` in the `scenarioPresets` array.

When adding a preset:

- Give every unit a stable `id`.
- Keep side names specific and readable.
- Set `strength` and `maxStrength`.
- Add traits that matter to the engine, such as `armor`, `artillery`, `elite`, `recon`, `pursuit`, and `breakthrough`.
- Choose an initial terrain that matches the typical opening battle.
- Add a starting attacker and defender stack so the preset can run immediately.
