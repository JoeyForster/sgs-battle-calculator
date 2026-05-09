# Data Model

The browser builds battle JSON and posts it to the FastAPI backend. The backend validates the payload with Pydantic and sends it to the pure Python engine.

## Endpoints

```text
GET  /
GET  /api/example
POST /api/validate
POST /api/simulate
```

`POST /api/validate` returns:

```json
{
  "valid": true,
  "errors": []
}
```

`POST /api/simulate` returns a full battle report with initial Battle Morale, round logs, final winner data, and survivor snapshots.

## Top-Level Payload

```json
{
  "meta": {},
  "battle": {},
  "attacker": {},
  "defender": {}
}
```

## Meta

| Field | Meaning |
| --- | --- |
| `scenario_name` | Display name for the scenario. |
| `turn_number` | Current turn number. |
| `date_label` | Human-readable turn/date label. |
| `active_side` | Side currently acting. |
| `phase` | Current game phase label. |
| `seed` | RNG seed used for deterministic dice. |

## Battle Settings

| Field | Meaning |
| --- | --- |
| `region` | Battle location name. |
| `terrain` | Terrain label. |
| `attacker_combat_modifier` | Combat modifier applied to attacker shots. |
| `defender_combat_modifier` | Combat modifier applied to defender shots. |
| `attacker_morale_modifier` | Morale modifier applied to attacker Battle Morale. |
| `defender_morale_modifier` | Morale modifier applied to defender Battle Morale. |
| `air_modifier` | Round modifier for air support. |
| `artillery_modifier` | Round modifier for artillery. |
| `mine_modifier` | Round modifier for mines. |
| `recon_modifier` | Round modifier for recon. |
| `connection_defender_modifier` | First-combat-round defender bonus. |
| `defender_entrenched` | Adds the entrenchment penalty against attackers. |
| `recon_allowed` | Enables or skips recon fire. |
| `pursuit_allowed` | Allows pursuit after rout when eligible. |
| `breakthrough_allowed` | Allows breakthrough eligibility after attacker victory. |
| `armor_superiority_allowed` | Enables armor superiority checks. |
| `max_next_rounds` | Number of extra battle phases, from `0` to `3`. |

## Side

| Field | Meaning |
| --- | --- |
| `name` | Side display name. Required and must not be blank. |
| `leader` | Optional leader object with combat and morale values. |
| `scenario_morale_bonus` | Side-level morale adjustment. |
| `boosters` | Always-on modifiers. |
| `modifiers` | Generic card or situation modifiers. |
| `retreat_policy` | Automated retreat behavior for this battle. |
| `units` | Units present for this side. Must include at least one surviving combat unit. |

## Unit

| Field | Meaning |
| --- | --- |
| `id` | Stable unique ID within the side. |
| `name` | Unit display name. |
| `role` | `combat` or `support`. |
| `domain` | `land`, `air`, or `sea`. |
| `attack` | Attack Factor, `0` to `9`. |
| `defense` | Defense Factor, `0` to `9`. |
| `morale` | Morale Factor, `0` to `9`. |
| `strength` | Current Health. |
| `max_strength` | Maximum Health. |
| `rof` | Rate of Fire, `1` to `5`. |
| `tags` | Trait strings used by the engine. |
| `loss_priority` | `first`, `normal`, or `last`. |

`strength` cannot exceed `max_strength`.

## Common Tags

| Tag | Engine use |
| --- | --- |
| `elite` | Rerolls first failed shot. |
| `armor`, `tank`, `cav`, `cavalry`, `mechanized` | Counts as cavalry/armor for hit allocation and armor checks. |
| `artillery` | Fires in artillery preparation. |
| `air`, `air_support`, `land_attack`, `fighter_bomber`, `dive_bomber` | Enables air support or air participation. |
| `mine`, `minefield` | Fires in the mines round. |
| `recon`, `reconnaissance` | Fires in the recon round. |
| `pursuit`, `breakthrough` | Enables pursuit fire and possible breakthrough. |

## Minimal Example

```json
{
  "meta": {
    "scenario_name": "Example",
    "turn_number": 1,
    "date_label": "Turn 1",
    "active_side": "Attackers",
    "phase": "Battles",
    "seed": 1
  },
  "battle": {
    "region": "Test Region",
    "terrain": "Clear",
    "max_next_rounds": 0
  },
  "attacker": {
    "name": "Attackers",
    "units": [
      {
        "id": "a-1",
        "name": "Attacking Infantry",
        "role": "combat",
        "domain": "land",
        "attack": 3,
        "defense": 3,
        "morale": 3,
        "strength": 3,
        "max_strength": 3,
        "rof": 1,
        "tags": ["infantry"],
        "loss_priority": "normal"
      }
    ]
  },
  "defender": {
    "name": "Defenders",
    "units": [
      {
        "id": "d-1",
        "name": "Defending Infantry",
        "role": "combat",
        "domain": "land",
        "attack": 3,
        "defense": 3,
        "morale": 3,
        "strength": 3,
        "max_strength": 3,
        "rof": 1,
        "tags": ["infantry"],
        "loss_priority": "normal"
      }
    ]
  }
}
```
