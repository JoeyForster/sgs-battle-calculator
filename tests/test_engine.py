from __future__ import annotations

from copy import deepcopy

import pytest
from pydantic import ValidationError

from sgs_calculator.engine import BattleSimulator, simulate_battle
from sgs_calculator.example import EXAMPLE_BATTLE
from sgs_calculator.models import BattleInput


def make_battle(
    *,
    seed: int = 1,
    attacker_units: list[dict] | None = None,
    defender_units: list[dict] | None = None,
    battle_overrides: dict | None = None,
    attacker_overrides: dict | None = None,
    defender_overrides: dict | None = None,
) -> dict:
    data = {
        "meta": {
            "scenario_name": "Test",
            "turn_number": 1,
            "date_label": "Turn 1",
            "active_side": "Attacker",
            "phase": "Battles",
            "seed": seed,
        },
        "battle": {
            "region": "Test Region",
            "terrain": "Clear",
            "max_next_rounds": 0,
        },
        "attacker": {
            "name": "Red",
            "leader": None,
            "boosters": [],
            "modifiers": [],
            "retreat_policy": {"mode": "never", "prevent_pursuit": True},
            "units": attacker_units
            or [
                {
                    "id": "red-1",
                    "name": "Red Infantry",
                    "role": "combat",
                    "domain": "land",
                    "attack": 3,
                    "defense": 3,
                    "morale": 3,
                    "strength": 3,
                    "max_strength": 3,
                    "rof": 1,
                    "tags": ["infantry"],
                    "loss_priority": "normal",
                }
            ],
        },
        "defender": {
            "name": "Blue",
            "leader": None,
            "boosters": [],
            "modifiers": [],
            "retreat_policy": {"mode": "never", "prevent_pursuit": True},
            "units": defender_units
            or [
                {
                    "id": "blue-1",
                    "name": "Blue Infantry",
                    "role": "combat",
                    "domain": "land",
                    "attack": 3,
                    "defense": 3,
                    "morale": 3,
                    "strength": 3,
                    "max_strength": 3,
                    "rof": 1,
                    "tags": ["infantry"],
                    "loss_priority": "normal",
                }
            ],
        },
    }
    data["battle"].update(battle_overrides or {})
    data["attacker"].update(attacker_overrides or {})
    data["defender"].update(defender_overrides or {})
    return data


def main_round(report):
    return next(round_report for round_report in report.rounds if round_report.name == "main")


def round_by_name(report, name: str):
    return next(round_report for round_report in report.rounds if round_report.name == name)


def unit_dict(
    unit_id: str,
    name: str | None = None,
    *,
    role: str = "combat",
    domain: str = "land",
    attack: int = 3,
    defense: int = 3,
    morale: int = 3,
    strength: int = 3,
    max_strength: int | None = None,
    rof: int = 1,
    tags: list[str] | None = None,
    loss_priority: str = "normal",
) -> dict:
    return {
        "id": unit_id,
        "name": name or unit_id,
        "role": role,
        "domain": domain,
        "attack": attack,
        "defense": defense,
        "morale": morale,
        "strength": strength,
        "max_strength": max_strength if max_strength is not None else strength,
        "rof": rof,
        "tags": tags or ["infantry"],
        "loss_priority": loss_priority,
    }


class RiggedRng:
    def __init__(self, *rolls: int):
        self.rolls = list(rolls)

    def randint(self, low: int, high: int) -> int:
        assert low == 0
        assert high == 9
        return self.rolls.pop(0)


def test_schema_rejects_duplicate_unit_ids() -> None:
    data = make_battle()
    data["attacker"]["units"].append(deepcopy(data["attacker"]["units"][0]))

    with pytest.raises(ValidationError):
        BattleInput.model_validate(data)


def test_schema_rejects_strength_above_maximum_health() -> None:
    data = make_battle(attacker_units=[unit_dict("red-1", strength=4, max_strength=3)])

    with pytest.raises(ValidationError, match="strength cannot exceed max_strength"):
        BattleInput.model_validate(data)


def test_schema_requires_at_least_one_surviving_combat_unit_per_side() -> None:
    data = make_battle(
        attacker_units=[
            unit_dict(
                "red-support",
                role="support",
                attack=4,
                defense=2,
                strength=2,
                tags=["artillery"],
                loss_priority="last",
            )
        ]
    )

    with pytest.raises(ValidationError, match="side must include at least one surviving combat unit"):
        BattleInput.model_validate(data)


def test_schema_normalizes_tags_and_removes_blank_tags() -> None:
    data = make_battle(attacker_units=[unit_dict("red-1", tags=[" Armor ", "", "ELITE"])])

    battle = BattleInput.model_validate(data)

    assert battle.attacker.units[0].tags == ["armor", "elite"]


def test_zero_roll_always_hits_even_with_zero_threshold() -> None:
    data = make_battle(
        seed=2,
        attacker_units=[
            {
                "id": "red-1",
                "name": "Red Low Factor",
                "role": "combat",
                "domain": "land",
                "attack": 0,
                "defense": 0,
                "morale": 3,
                "strength": 3,
                "max_strength": 3,
                "rof": 1,
                "tags": ["infantry"],
                "loss_priority": "normal",
            }
        ],
    )

    report = simulate_battle(BattleInput.model_validate(data))
    shot = next(shot for shot in main_round(report).shots if shot.side == "attacker")

    assert shot.roll == 0
    assert shot.threshold == 0
    assert shot.hit is True


def test_negative_modified_factor_only_hits_on_natural_zero() -> None:
    data = make_battle(
        attacker_units=[unit_dict("red-low", attack=0)],
        battle_overrides={"attacker_combat_modifier": -5},
    )
    simulator = BattleSimulator(BattleInput.model_validate(data))
    unit = simulator.sides["attacker"].units[0]
    simulator.rng = RiggedRng(1, 0)

    miss, miss_hit = simulator._roll_shot("attacker", unit, "main", 1)
    natural_zero, zero_hit = simulator._roll_shot("attacker", unit, "main", 2)

    assert miss.modified_factor == -5
    assert miss.threshold == 0
    assert miss_hit is False
    assert natural_zero.threshold == 0
    assert zero_hit is True


def test_high_modified_factor_clamps_threshold_to_nine() -> None:
    data = make_battle(
        attacker_units=[unit_dict("red-high", attack=9)],
        battle_overrides={"attacker_combat_modifier": 5},
    )
    simulator = BattleSimulator(BattleInput.model_validate(data))
    unit = simulator.sides["attacker"].units[0]
    simulator.rng = RiggedRng(9)

    shot, hit = simulator._roll_shot("attacker", unit, "main", 1)

    assert shot.modified_factor == 14
    assert shot.threshold == 9
    assert hit is True


def test_rate_of_fire_creates_one_shot_per_fire_rate() -> None:
    data = make_battle(
        seed=5,
        attacker_units=[unit_dict("red-rof", attack=0, rof=3, morale=9)],
        defender_units=[unit_dict("blue-1", attack=0, defense=0, morale=9)],
    )

    report = simulate_battle(BattleInput.model_validate(data))
    attacker_shots = [shot for shot in main_round(report).shots if shot.side == "attacker"]

    assert len(attacker_shots) == 3
    assert [shot.shot_number for shot in attacker_shots] == [1, 2, 3]


def test_elite_unit_rerolls_failed_shot() -> None:
    data = make_battle(
        seed=5,
        attacker_units=[
            {
                "id": "red-elite",
                "name": "Red Elite",
                "role": "combat",
                "domain": "land",
                "attack": 8,
                "defense": 3,
                "morale": 4,
                "strength": 3,
                "max_strength": 3,
                "rof": 1,
                "tags": ["infantry", "elite"],
                "loss_priority": "normal",
            }
        ],
    )

    report = simulate_battle(BattleInput.model_validate(data))
    attacker_shots = [shot for shot in main_round(report).shots if shot.side == "attacker"]

    assert [shot.roll for shot in attacker_shots] == [9, 4]
    assert attacker_shots[0].hit is False
    assert attacker_shots[1].reroll_of == 9
    assert attacker_shots[1].hit is True


def test_round_shooter_selection_matches_unit_traits() -> None:
    data = make_battle(
        attacker_units=[
            unit_dict("red-line", tags=["infantry"]),
            unit_dict("red-art", role="support", tags=["artillery"], loss_priority="last"),
            unit_dict("red-air", domain="air", tags=["air", "air_support", "land_attack"]),
            unit_dict("red-mine", role="support", tags=["minefield"], loss_priority="first"),
            unit_dict("red-recon", tags=["recon"]),
        ]
    )
    simulator = BattleSimulator(BattleInput.model_validate(data))

    assert [unit.id for unit in simulator._shooters("attacker", "artillery")] == ["red-art"]
    assert [unit.id for unit in simulator._shooters("attacker", "air_support")] == ["red-air"]
    assert [unit.id for unit in simulator._shooters("attacker", "mines")] == ["red-mine"]
    assert [unit.id for unit in simulator._shooters("attacker", "recon")] == ["red-recon"]
    assert [unit.id for unit in simulator._shooters("attacker", "main")] == [
        "red-line",
        "red-air",
        "red-recon",
    ]


def test_recon_round_is_skipped_when_recon_is_not_allowed() -> None:
    data = make_battle(
        attacker_units=[unit_dict("red-recon", tags=["recon"])],
        battle_overrides={"recon_allowed": False, "max_next_rounds": 0},
    )

    report = simulate_battle(BattleInput.model_validate(data))

    assert "recon" not in [round_report.name for round_report in report.rounds]


def test_air_unit_needs_land_attack_trait_to_fire_in_main_round() -> None:
    data = make_battle(
        attacker_units=[
            unit_dict("red-fighter", domain="air", tags=["air", "fighter"]),
            unit_dict("red-cas", domain="air", tags=["air", "air_support", "land_attack"]),
        ]
    )
    simulator = BattleSimulator(BattleInput.model_validate(data))

    assert [unit.id for unit in simulator._shooters("attacker", "main")] == ["red-cas"]


def test_modifier_stack_includes_leader_terrain_entrenchment_booster_and_armor_superiority() -> None:
    data = make_battle(
        attacker_units=[
            {
                "id": "red-tank-1",
                "name": "Red Tank 1",
                "role": "combat",
                "domain": "land",
                "attack": 3,
                "defense": 3,
                "morale": 4,
                "strength": 3,
                "max_strength": 3,
                "rof": 1,
                "tags": ["armor"],
                "loss_priority": "normal",
            },
            {
                "id": "red-tank-2",
                "name": "Red Tank 2",
                "role": "combat",
                "domain": "land",
                "attack": 3,
                "defense": 3,
                "morale": 4,
                "strength": 3,
                "max_strength": 3,
                "rof": 1,
                "tags": ["armor"],
                "loss_priority": "normal",
            },
        ],
        battle_overrides={"attacker_combat_modifier": -1, "defender_entrenched": True},
        attacker_overrides={
            "leader": {"name": "Red Leader", "combat": 3, "morale": 0},
            "boosters": [{"name": "HQ", "attack": 1}],
        },
        defender_overrides={"leader": {"name": "Blue Leader", "combat": 1, "morale": 0}},
    )
    simulator = BattleSimulator(BattleInput.model_validate(data))
    unit = simulator.sides["attacker"].units[0]

    factor = simulator._modified_combat_factor("attacker", unit, "main")

    assert factor == 5


def test_modifier_filters_by_round_and_tag() -> None:
    data = make_battle(
        attacker_units=[unit_dict("red-tank", attack=3, tags=["armor"])],
        attacker_overrides={
            "modifiers": [
                {"name": "Armor Main", "attack": 2, "rounds": ["main"], "tags": ["armor"]},
                {"name": "Wrong Round", "attack": 5, "rounds": ["artillery"], "tags": ["armor"]},
                {"name": "Wrong Tag", "attack": 7, "rounds": ["main"], "tags": ["infantry"]},
                {"name": "General Combat", "combat": 1},
            ]
        },
    )
    simulator = BattleSimulator(BattleInput.model_validate(data))
    unit = simulator.sides["attacker"].units[0]

    assert simulator._modified_combat_factor("attacker", unit, "main") == 6
    assert simulator._modified_combat_factor("attacker", unit, "artillery") == 9


def test_defender_uses_defense_modifiers_not_attack_modifiers() -> None:
    data = make_battle(
        defender_units=[unit_dict("blue-1", defense=3)],
        defender_overrides={
            "modifiers": [
                {"name": "Defensive Ground", "attack": 9, "defense": 2, "rounds": ["main"]}
            ]
        },
    )
    simulator = BattleSimulator(BattleInput.model_validate(data))
    unit = simulator.sides["defender"].units[0]

    assert simulator._modified_combat_factor("defender", unit, "main") == 5


def test_defender_connection_modifier_applies_only_to_first_combat_round() -> None:
    data = make_battle(
        defender_units=[unit_dict("blue-1", defense=3)],
        battle_overrides={"connection_defender_modifier": 2},
    )
    simulator = BattleSimulator(BattleInput.model_validate(data))
    unit = simulator.sides["defender"].units[0]

    assert simulator._modified_combat_factor("defender", unit, "main") == 5

    simulator.first_combat_round = False

    assert simulator._modified_combat_factor("defender", unit, "main") == 3


def test_armor_superiority_requires_two_units_two_to_one_and_enabled_rule() -> None:
    attacker_units = [
        unit_dict("red-tank-1", tags=["armor"]),
        unit_dict("red-tank-2", tags=["armor"]),
    ]
    defender_units = [unit_dict("blue-tank", tags=["armor"])]
    enabled = BattleSimulator(
        BattleInput.model_validate(
            make_battle(attacker_units=attacker_units, defender_units=defender_units)
        )
    )
    disabled = BattleSimulator(
        BattleInput.model_validate(
            make_battle(
                attacker_units=attacker_units,
                defender_units=defender_units,
                battle_overrides={"armor_superiority_allowed": False},
            )
        )
    )
    only_one_tank = BattleSimulator(
        BattleInput.model_validate(
            make_battle(
                attacker_units=[unit_dict("red-tank-1", tags=["armor"])],
                defender_units=[unit_dict("blue-infantry", tags=["infantry"])],
            )
        )
    )

    assert enabled._has_armor_superiority("attacker") is True
    assert disabled._has_armor_superiority("attacker") is False
    assert only_one_tank._has_armor_superiority("attacker") is False


def test_battle_morale_breakdown() -> None:
    data = make_battle(
        attacker_units=[
            {
                "id": "red-tank",
                "name": "Red Tank",
                "role": "combat",
                "domain": "land",
                "attack": 3,
                "defense": 3,
                "morale": 3,
                "strength": 3,
                "max_strength": 3,
                "rof": 1,
                "tags": ["armor"],
                "loss_priority": "normal",
            },
            {
                "id": "red-plane",
                "name": "Red Plane",
                "role": "combat",
                "domain": "air",
                "attack": 3,
                "defense": 3,
                "morale": 5,
                "strength": 2,
                "max_strength": 2,
                "rof": 1,
                "tags": ["air", "land_attack"],
                "loss_priority": "normal",
            },
        ],
        battle_overrides={"attacker_morale_modifier": 1},
        attacker_overrides={
            "leader": {"name": "Red Leader", "combat": 0, "morale": 2},
            "scenario_morale_bonus": 1,
            "boosters": [{"name": "Morale HQ", "morale": 1}],
        },
    )

    report = simulate_battle(BattleInput.model_validate(data))

    assert report.initial_battle_morale["attacker"].total == 11


def test_battle_morale_average_rounds_half_up_and_excludes_support_units() -> None:
    data = make_battle(
        attacker_units=[
            unit_dict("red-low", morale=2),
            unit_dict("red-high", morale=3),
            unit_dict(
                "red-support",
                role="support",
                morale=9,
                tags=["artillery"],
                loss_priority="last",
            ),
        ]
    )

    report = simulate_battle(BattleInput.model_validate(data))

    assert report.initial_battle_morale["attacker"].average_combat_morale == 3


def test_next_round_exhaustion_reduces_battle_morale_for_both_sides() -> None:
    simulator = BattleSimulator(BattleInput.model_validate(make_battle()))
    simulator._initialize_battle_morale()
    initial = {side: simulator.sides[side].current_bm for side in ("attacker", "defender")}

    events = simulator._apply_next_round_exhaustion(1)

    assert simulator.sides["attacker"].current_bm == initial["attacker"] - 1
    assert simulator.sides["defender"].current_bm == initial["defender"] - 1
    assert events == [
        "Next 1 battle exhaustion: Red BM -1.",
        "Next 1 battle exhaustion: Blue BM -1.",
    ]


def test_heavy_losses_reduce_battle_morale_once_for_the_round() -> None:
    data = make_battle(attacker_units=[unit_dict("red-1", strength=4, max_strength=4)])
    simulator = BattleSimulator(BattleInput.model_validate(data))
    simulator._initialize_battle_morale()
    start_bm = simulator.sides["attacker"].current_bm
    simulator.sides["attacker"].units[0].strength = 1
    events: list[str] = []

    simulator._apply_heavy_loss_checks(
        {"attacker": 4, "defender": 0},
        {"attacker": {"red-1": 4}, "defender": {}},
        events,
    )

    assert simulator.sides["attacker"].current_bm == start_bm - 1
    assert events == ["Red suffers heavy losses (3/4 SP); BM -1."]


def test_other_hits_against_only_cav_are_halved_with_wastage() -> None:
    data = make_battle(
        defender_units=[
            {
                "id": "blue-tank",
                "name": "Blue Tank",
                "role": "combat",
                "domain": "land",
                "attack": 3,
                "defense": 3,
                "morale": 3,
                "strength": 4,
                "max_strength": 4,
                "rof": 1,
                "tags": ["armor"],
                "loss_priority": "normal",
            }
        ]
    )
    simulator = BattleSimulator(BattleInput.model_validate(data))

    allocations, wasted = simulator._allocate_hits("defender", {"cav": 0, "other": 3})

    assert sum(allocations.values()) == 1
    assert wasted == 2


def test_loss_priority_first_absorbs_hits_before_normal_and_last() -> None:
    data = make_battle(
        defender_units=[
            unit_dict("blue-first", strength=2, loss_priority="first"),
            unit_dict("blue-normal", strength=2, loss_priority="normal"),
            unit_dict("blue-last", strength=2, loss_priority="last"),
        ]
    )
    simulator = BattleSimulator(BattleInput.model_validate(data))

    allocations, wasted = simulator._allocate_hits("defender", {"cav": 0, "other": 3})

    assert allocations == {"blue-first": 2, "blue-normal": 1}
    assert wasted == 0


def test_hits_distribute_proportionally_by_remaining_strength() -> None:
    data = make_battle(
        defender_units=[
            unit_dict("blue-large", strength=4),
            unit_dict("blue-small", strength=2),
        ]
    )
    simulator = BattleSimulator(BattleInput.model_validate(data))

    allocations, wasted = simulator._allocate_hits("defender", {"cav": 0, "other": 3})

    assert allocations == {"blue-large": 2, "blue-small": 1}
    assert wasted == 0


def test_cav_hits_target_cav_first_then_fall_back_to_other_units() -> None:
    data = make_battle(
        defender_units=[
            unit_dict("blue-tank", strength=1, tags=["armor"]),
            unit_dict("blue-infantry", strength=2, tags=["infantry"]),
        ]
    )
    simulator = BattleSimulator(BattleInput.model_validate(data))

    allocations, wasted = simulator._allocate_hits("defender", {"cav": 3, "other": 0})

    assert allocations == {"blue-tank": 1, "blue-infantry": 2}
    assert wasted == 0


def test_panicked_units_are_not_hit_again_until_pursuit() -> None:
    data = make_battle(defender_units=[unit_dict("blue-panicked", strength=2)])
    simulator = BattleSimulator(BattleInput.model_validate(data))
    simulator.sides["defender"].units[0].panicked = True

    normal_allocations, normal_wasted = simulator._allocate_hits(
        "defender", {"cav": 0, "other": 1}
    )
    pursuit_allocations, pursuit_wasted = simulator._allocate_hits(
        "defender", {"cav": 0, "other": 1}, include_panicked=True
    )

    assert normal_allocations == {}
    assert normal_wasted == 1
    assert pursuit_allocations == {"blue-panicked": 1}
    assert pursuit_wasted == 0


def test_destroyed_unit_reduces_battle_morale_only_once() -> None:
    data = make_battle(defender_units=[unit_dict("blue-1", strength=1)])
    simulator = BattleSimulator(BattleInput.model_validate(data))
    simulator._initialize_battle_morale()
    start_bm = simulator.sides["defender"].current_bm
    events: list[str] = []

    simulator._apply_hits(
        {"attacker": {}, "defender": {"blue-1": 2}},
        {"attacker": {}, "defender": {"blue-1": 1}},
        events,
        "main",
    )
    simulator._apply_hits(
        {"attacker": {}, "defender": {"blue-1": 2}},
        {"attacker": {}, "defender": {"blue-1": 0}},
        events,
        "main",
    )

    assert simulator.sides["defender"].current_bm == start_bm - 1
    assert simulator.sides["defender"].losses_count == 1


def test_panic_check_removes_unit_from_battlefield() -> None:
    data = make_battle(
        seed=1,
        attacker_units=[
            {
                "id": "red-guns",
                "name": "Red Guns",
                "role": "combat",
                "domain": "land",
                "attack": 9,
                "defense": 1,
                "morale": 3,
                "strength": 3,
                "max_strength": 3,
                "rof": 2,
                "tags": ["infantry"],
                "loss_priority": "normal",
            }
        ],
        defender_units=[
            {
                "id": "blue-green",
                "name": "Blue Green Troops",
                "role": "combat",
                "domain": "land",
                "attack": 0,
                "defense": 0,
                "morale": 0,
                "strength": 4,
                "max_strength": 4,
                "rof": 1,
                "tags": ["infantry"],
                "loss_priority": "normal",
            }
        ],
    )

    report = simulate_battle(BattleInput.model_validate(data))
    defender = report.survivors["defender"][0]

    assert defender.strength == 2
    assert defender.panicked is True
    assert report.final.winner_key == "attacker"


def test_panic_check_passes_on_roll_equal_to_threshold() -> None:
    data = make_battle(defender_units=[unit_dict("blue-1", morale=2, strength=4)])
    simulator = BattleSimulator(BattleInput.model_validate(data))
    simulator._initialize_battle_morale()
    simulator.rng = RiggedRng(4)
    events: list[str] = []

    simulator._apply_panic_checks(
        {"attacker": {}, "defender": {"blue-1": 2}},
        {"attacker": {}, "defender": {"blue-1": 4}},
        events,
    )

    assert simulator.sides["defender"].units[0].panicked is False
    assert events == ["Blue blue-1 holds cohesion (panic roll 4 <= 4)."]


def test_both_sides_demoralized_equally_skip_rout_test() -> None:
    simulator = BattleSimulator(BattleInput.model_validate(make_battle()))
    simulator._initialize_battle_morale()
    simulator.sides["attacker"].current_bm = 0
    simulator.sides["defender"].current_bm = 0
    report = simulator._empty_round("main", 1, "Main", [])

    simulator._check_end_after_round(report)

    assert simulator.routed_side is None
    assert report.events == ["Both sides are demoralized equally; no rout test is made."]


def test_rout_roll_zero_passes_even_with_negative_battle_morale() -> None:
    simulator = BattleSimulator(BattleInput.model_validate(make_battle()))
    simulator._initialize_battle_morale()
    simulator.sides["attacker"].current_bm = -2
    simulator.rng = RiggedRng(0)
    events: list[str] = []

    simulator._rout_test("attacker", events)

    assert simulator.routed_side is None
    assert events == ["Red passes rout test (roll 0, BM -2)."]


def test_rout_can_trigger_pursuit() -> None:
    data = make_battle(
        seed=1,
        battle_overrides={"defender_morale_modifier": -10, "pursuit_allowed": True},
        attacker_units=[
            {
                "id": "red-tank",
                "name": "Red Tank",
                "role": "combat",
                "domain": "land",
                "attack": 0,
                "defense": 1,
                "morale": 8,
                "strength": 3,
                "max_strength": 3,
                "rof": 1,
                "tags": ["armor", "pursuit"],
                "loss_priority": "normal",
            }
        ],
        defender_units=[
            {
                "id": "blue-stubborn",
                "name": "Blue Stubborn",
                "role": "combat",
                "domain": "land",
                "attack": 0,
                "defense": 0,
                "morale": 9,
                "strength": 3,
                "max_strength": 3,
                "rof": 1,
                "tags": ["infantry"],
                "loss_priority": "normal",
            }
        ],
    )

    report = simulate_battle(BattleInput.model_validate(data))

    assert report.final.routed_side == "defender"
    assert report.final.pursuit_happened is True
    assert report.rounds[-1].name == "pursuit"


def test_voluntary_retreat_before_phase_gives_win_without_pursuit() -> None:
    data = make_battle(
        seed=5,
        battle_overrides={"max_next_rounds": 1, "pursuit_allowed": True},
        attacker_units=[unit_dict("red-tank", attack=0, morale=9, tags=["armor", "pursuit"])],
        defender_units=[unit_dict("blue-1", attack=0, defense=0, morale=9)],
        defender_overrides={
            "retreat_policy": {"mode": "after_main", "prevent_pursuit": True}
        },
    )

    report = simulate_battle(BattleInput.model_validate(data))

    assert report.final.winner_key == "attacker"
    assert report.final.retreated_side == "defender"
    assert report.final.pursuit_happened is False
    assert round_by_name(report, "next").shots == []


def test_breakthrough_requires_attacking_winner_enabled_terrain_and_eligible_unit() -> None:
    data = make_battle(attacker_units=[unit_dict("red-fast", tags=["breakthrough"])])
    simulator = BattleSimulator(BattleInput.model_validate(data))

    assert simulator._breakthrough_available("attacker") is True
    assert simulator._breakthrough_available("defender") is False

    disabled = BattleSimulator(
        BattleInput.model_validate(
            make_battle(
                attacker_units=[unit_dict("red-fast", tags=["breakthrough"])],
                battle_overrides={"breakthrough_allowed": False},
            )
        )
    )

    assert disabled._breakthrough_available("attacker") is False


def test_total_elimination_removes_half_of_surviving_support_units() -> None:
    data = make_battle(
        defender_units=[
            unit_dict("blue-combat", strength=1),
            unit_dict("blue-support-1", role="support", tags=["artillery"], loss_priority="last"),
            unit_dict("blue-support-2", role="support", tags=["artillery"], loss_priority="last"),
            unit_dict("blue-support-3", role="support", tags=["artillery"], loss_priority="last"),
        ]
    )
    simulator = BattleSimulator(BattleInput.model_validate(data))
    combat = simulator.sides["defender"].units[0]
    combat.strength = 0
    combat.destroyed = True

    events = simulator._apply_total_elimination()

    destroyed_support = [
        unit for unit in simulator.sides["defender"].units[1:] if unit.destroyed
    ]
    assert len(destroyed_support) == 1
    assert events == ["Total elimination removes support unit Blue blue-support-1."]


def test_example_battle_golden_result() -> None:
    report = simulate_battle(BattleInput.model_validate(EXAMPLE_BATTLE))

    assert report.final.model_dump() == {
        "winner": "Commonwealth",
        "winner_key": "defender",
        "loser": "Axis",
        "loser_key": "attacker",
        "reason": "defender holds after the final battle round",
        "routed_side": None,
        "retreated_side": None,
        "pursuit_happened": False,
        "breakthrough_available": False,
    }
    assert [round_report.label for round_report in report.rounds] == [
        "Setup",
        "Artillery Preparation",
        "Air Support",
        "Mines",
        "Main",
        "Next 1",
        "Next 2",
        "Next 3",
    ]
    assert report.rounds[-1].hits_taken == {"attacker": 0, "defender": 3}
