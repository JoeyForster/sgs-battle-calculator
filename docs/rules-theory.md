# Rules Theory

## Philosophy

The engine models the battle-core math that is useful during live SGS play. It does not try to replace the board state, player decisions, map movement, supply, or the full card deck. Those remain manual.

The browser stores the current campaign-style state. The Python engine receives one battle payload, resolves it deterministically from the seed, and returns a report with every round, roll, morale change, and surviving unit.

## Battle Flow

The implemented round order is:

1. Setup.
2. Artillery preparation.
3. Air support.
4. Mines.
5. Recon.
6. Main combat.
7. Up to three extra battle phases.
8. Pursuit, when a routed enemy and terrain allow it.

The engine still uses the internal key `next` for those extra rounds because the original schema used that name. The UI displays them as `Phase` rounds.

## D10 Shot Theory

Each eligible unit fires a number of shots equal to its Rate of Fire.

For every shot:

- Roll one D10 as a value from `0` to `9`.
- A roll of `0` always hits.
- Otherwise the shot hits when `roll <= modified combat factor`.
- The final hit threshold is clamped between `0` and `9`.
- Elite units reroll their first failed shot.

Attackers use Attack Factor. Defenders use Defense Factor.

## Combat Factor Modifiers

The modified combat factor is built from:

- Unit Attack Factor or Defense Factor.
- Leader combat advantage over the opposing leader.
- Terrain combat modifier.
- Round modifier for artillery, air support, mines, or recon.
- Active side modifiers from boosters or cards.
- Entrenchment penalty against attackers.
- Defender connection modifier during the first combat round.
- Armor superiority bonus when enabled.

## Battle Morale

Initial Battle Morale is:

```text
average combat-unit morale
+ leader morale
+ terrain morale modifier
+ scenario morale bonus
+ air presence bonus
+ armor presence bonus
+ armor superiority bonus
+ booster/card morale modifiers
```

Average morale is rounded half up.

Battle Morale can drop during battle:

- Eliminated units reduce Battle Morale by 1.
- Panicked units reduce Battle Morale by 1.
- Heavy losses in a round reduce Battle Morale by 1.
- Each extra battle phase exhausts both sides by 1 Battle Morale.

## Panic And Rout

A unit checks panic when it takes at least half of its starting strength in hits during a round and survives.

The panic threshold is:

```text
unit morale * 2
```

The unit holds if the D10 roll is less than or equal to that threshold. Otherwise it panics, leaves the active battlefield, and costs the side 1 Battle Morale.

When a side reaches Battle Morale `<= 0`, it may need a rout check:

- A roll of `0` passes.
- Otherwise it passes only when `roll <= current Battle Morale`.
- A failed check routs that side and usually makes the opponent the winner.

## Hit Allocation

Shots are grouped by the firing unit:

- Cavalry/armor/mechanized style units inflict `cav` hits.
- Other units inflict `other` hits.

Allocation theory:

- Cavalry hits try to hit cavalry/armor targets first, then other targets.
- Other hits try to hit non-cavalry targets first.
- If only cavalry/armor targets remain, other hits are halved and the remainder is wasted.
- Hits respect unit loss priority: `first`, then `normal`, then `last`.
- Hits are distributed proportionally by remaining strength within each priority group.

## Winner Selection

The attacker wins when the defender has no active combat units, voluntarily retreats, or routs.

The defender wins when the attacker has no active combat units, voluntarily retreats, routs, or when all allowed battle rounds end without an attacker victory.

Breakthrough can become available for an attacking winner when terrain allows breakthrough and at least one surviving attacker has a pursuit/breakthrough-capable trait.

## V1 Assumptions

- The engine resolves one battle at a time.
- Start time is reporting metadata, not an event scheduler.
- Cards are represented as generic modifiers, not a shuffled deck.
- Preset rosters are editable starter data, not a claim that every counter in a boxed scenario has been fully encoded.
- Movement, supply, sieges, naval combat, and map breakthrough movement are deferred.
- The rule implementation should stay testable as pure Python, with the UI acting as a stateful manual input layer.
