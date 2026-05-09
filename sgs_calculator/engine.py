from __future__ import annotations

from dataclasses import dataclass
from math import ceil, floor
import random
from typing import Iterable

from .models import (
    BattleInput,
    FinalReport,
    LossPriority,
    MoraleBreakdown,
    RoundName,
    RoundReport,
    ShotRoll,
    SideInput,
    SideKey,
    SimulationReport,
    UnitDomain,
    UnitInput,
    UnitRole,
    UnitSnapshot,
)


SIDE_KEYS: tuple[SideKey, SideKey] = ("attacker", "defender")
OPPONENT: dict[SideKey, SideKey] = {"attacker": "defender", "defender": "attacker"}
CAV_TAGS = {"armor", "armour", "tank", "cav", "cavalry", "mechanized", "mechanised"}
AIR_SUPPORT_TAGS = {"air", "air_support", "land_attack", "fighter_bomber", "dive_bomber"}
PURSUIT_TAGS = {"pursuit", "breakthrough", *CAV_TAGS}
MAIN_AIR_TAGS = {"land_attack", "fighter_bomber", "dive_bomber"}


@dataclass
class UnitState:
    source: UnitInput
    side: SideKey
    strength: int
    destroyed: bool = False
    panicked: bool = False

    @property
    def id(self) -> str:
        return self.source.id

    @property
    def name(self) -> str:
        return self.source.name

    @property
    def tags(self) -> set[str]:
        return set(self.source.tags)

    def snapshot(self) -> UnitSnapshot:
        return UnitSnapshot(
            id=self.source.id,
            name=self.source.name,
            side=self.side,
            role=self.source.role,
            domain=self.source.domain,
            strength=self.strength,
            max_strength=self.source.max_strength,
            morale=self.source.morale,
            tags=list(self.source.tags),
            loss_priority=self.source.loss_priority,
            destroyed=self.destroyed,
            panicked=self.panicked,
        )


@dataclass
class SideState:
    key: SideKey
    source: SideInput
    units: list[UnitState]
    current_bm: int = 0
    initial_bm: MoraleBreakdown | None = None
    losses_count: int = 0
    panic_count: int = 0
    routed: bool = False
    retreated: bool = False


def simulate_battle(battle: BattleInput) -> SimulationReport:
    return BattleSimulator(battle).simulate()


class BattleSimulator:
    def __init__(self, battle: BattleInput):
        self.battle = battle
        self.rng = random.Random(battle.meta.seed)
        self.sides: dict[SideKey, SideState] = {
            "attacker": self._make_side("attacker", battle.attacker),
            "defender": self._make_side("defender", battle.defender),
        }
        self.first_combat_round = True
        self.routed_side: SideKey | None = None
        self.retreated_side: SideKey | None = None
        self.finished_reason = ""
        self.pursuit_happened = False

    def simulate(self) -> SimulationReport:
        self._initialize_battle_morale()
        rounds: list[RoundReport] = [self._setup_report()]

        for round_name in ("artillery", "air_support", "mines", "recon", "main"):
            if round_name == "recon" and not self.battle.battle.recon_allowed:
                continue
            if round_name != "main" and not self._round_has_shooters(round_name):
                continue
            if self._battle_finished():
                break
            report = self._resolve_round(round_name, len(rounds), self._round_label(round_name))
            rounds.append(report)
            self._check_end_after_round(report)
            if self._battle_finished():
                break

        if not self._battle_finished():
            for next_number in range(1, self.battle.battle.max_next_rounds + 1):
                if self._battle_finished():
                    break
                events = self._apply_next_round_exhaustion(next_number)
                retreated = self._maybe_retreat_before_next(next_number, events)
                if retreated:
                    rounds.append(self._empty_round("next", len(rounds), f"Next {next_number}", events))
                    break
                report = self._resolve_round("next", len(rounds), f"Next {next_number}", events)
                rounds.append(report)
                self._check_end_after_round(report)

        if not self._battle_finished():
            self.finished_reason = "defender holds after the final battle round"

        if self._should_run_pursuit():
            pursuit = self._resolve_round("pursuit", len(rounds), "Pursuit")
            self.pursuit_happened = True
            pursuit.events.insert(0, f"{self._side_name(self._winner_key())} conducts pursuit fire.")
            rounds.append(pursuit)

        total_elimination_events = self._apply_total_elimination()
        if total_elimination_events:
            rounds[-1].events.extend(total_elimination_events)
            rounds[-1].units = self._snapshots_by_side()

        final = self._final_report()
        return SimulationReport(
            meta=self.battle.meta,
            battle=self.battle.battle,
            initial_battle_morale={
                "attacker": self.sides["attacker"].initial_bm,
                "defender": self.sides["defender"].initial_bm,
            },
            rounds=rounds,
            final=final,
            survivors=self._snapshots_by_side(),
        )

    def _make_side(self, key: SideKey, source: SideInput) -> SideState:
        return SideState(
            key=key,
            source=source,
            units=[
                UnitState(unit, key, unit.strength, destroyed=unit.strength <= 0)
                for unit in source.units
            ],
        )

    def _initialize_battle_morale(self) -> None:
        for key in SIDE_KEYS:
            breakdown = self._battle_morale_breakdown(key)
            self.sides[key].current_bm = breakdown.total
            self.sides[key].initial_bm = breakdown

    def _battle_morale_breakdown(self, key: SideKey) -> MoraleBreakdown:
        side = self.sides[key]
        combat_units = [
            unit for unit in side.units if unit.source.role == UnitRole.combat and unit.strength > 0
        ]
        average = round_half_up(
            sum(unit.source.morale for unit in combat_units) / max(len(combat_units), 1)
        )
        leader_morale = side.source.leader.morale if side.source.leader else 0
        terrain = (
            self.battle.battle.attacker_morale_modifier
            if key == "attacker"
            else self.battle.battle.defender_morale_modifier
        )
        air_presence = 1 if any(self._is_air_unit(unit) for unit in combat_units) else 0
        armor_presence = 1 if any(self._is_armor_unit(unit) for unit in combat_units) else 0
        armor_superiority = 1 if self._has_armor_superiority(key) else 0
        modifiers = sum(modifier.morale for modifier in side.source.boosters + side.source.modifiers)
        total = (
            average
            + leader_morale
            + terrain
            + side.source.scenario_morale_bonus
            + air_presence
            + armor_presence
            + armor_superiority
            + modifiers
        )
        return MoraleBreakdown(
            total=total,
            average_combat_morale=average,
            leader_morale=leader_morale,
            terrain=terrain,
            scenario=side.source.scenario_morale_bonus,
            air_presence=air_presence,
            armor_presence=armor_presence,
            armor_superiority=armor_superiority,
            modifiers=modifiers,
        )

    def _setup_report(self) -> RoundReport:
        events = [
            f"Battle opens in {self.battle.battle.region} ({self.battle.battle.terrain}).",
            (
                f"Initial BM: attacker {self.sides['attacker'].current_bm}, "
                f"defender {self.sides['defender'].current_bm}."
            ),
        ]
        if self.battle.battle.defender_entrenched:
            events.append("Defender is entrenched; attacker combat factors suffer -1.")
        if self.battle.battle.connection_defender_modifier:
            events.append(
                "Defender receives connection modifier "
                f"+{self.battle.battle.connection_defender_modifier} in the first combat round."
            )
        return self._empty_round("setup", 0, "Setup", events)

    def _resolve_round(
        self,
        round_name: RoundName,
        index: int,
        label: str,
        initial_events: list[str] | None = None,
    ) -> RoundReport:
        events = list(initial_events or [])
        start_strengths = self._start_strengths(include_panicked=round_name == "pursuit")
        start_totals = {
            key: sum(start_strengths[key].values())
            for key in SIDE_KEYS
        }
        shots: list[ShotRoll] = []
        hits_inflicted: dict[SideKey, dict[str, int]] = {
            "attacker": {"cav": 0, "other": 0},
            "defender": {"cav": 0, "other": 0},
        }

        firing_sides: Iterable[SideKey] = SIDE_KEYS
        if round_name == "pursuit":
            firing_sides = (self._winner_key(),)

        for side_key in firing_sides:
            for unit in self._shooters(side_key, round_name):
                for shot_number in range(1, unit.source.rof + 1):
                    shot, hit = self._roll_shot(side_key, unit, round_name, shot_number)
                    shots.append(shot)
                    if not hit and "elite" in unit.tags:
                        reroll, hit = self._roll_shot(
                            side_key,
                            unit,
                            round_name,
                            shot_number,
                            reroll_of=shot.roll,
                        )
                        shots.append(reroll)
                    if hit:
                        hit_group = self._hit_group(unit)
                        hits_inflicted[side_key][hit_group] += 1

        hits_taken: dict[SideKey, int] = {"attacker": 0, "defender": 0}
        applied_hits_by_unit: dict[SideKey, dict[str, int]] = {"attacker": {}, "defender": {}}
        for target_key in SIDE_KEYS:
            source_key = OPPONENT[target_key]
            allocations, wasted = self._allocate_hits(
                target_key,
                hits_inflicted[source_key],
                include_panicked=round_name == "pursuit",
            )
            applied_hits_by_unit[target_key] = allocations
            hits_taken[target_key] = sum(allocations.values())
            if wasted:
                events.append(
                    f"{self._side_name(source_key)} wastes {wasted} hit(s) with no eligible target."
                )

        self._apply_hits(applied_hits_by_unit, start_strengths, events, round_name)
        if round_name != "pursuit":
            self._apply_panic_checks(applied_hits_by_unit, start_strengths, events)
            self._apply_heavy_loss_checks(start_totals, start_strengths, events)

        if self.first_combat_round and (shots or round_name == "main"):
            self.first_combat_round = False

        return RoundReport(
            name=round_name,
            label=label,
            index=index,
            events=events,
            shots=shots,
            hits_inflicted=hits_inflicted,
            hits_taken=hits_taken,
            morale={key: self.sides[key].current_bm for key in SIDE_KEYS},
            units=self._snapshots_by_side(),
        )

    def _roll_shot(
        self,
        side_key: SideKey,
        unit: UnitState,
        round_name: RoundName,
        shot_number: int,
        reroll_of: int | None = None,
    ) -> tuple[ShotRoll, bool]:
        modified_factor = self._modified_combat_factor(side_key, unit, round_name)
        threshold = max(0, min(9, modified_factor))
        roll = self.rng.randint(0, 9)
        hit = roll == 0 or roll <= threshold
        shot = ShotRoll(
            side=side_key,
            unit_id=unit.id,
            unit_name=unit.name,
            round=round_name,
            shot_number=shot_number,
            roll=roll,
            modified_factor=modified_factor,
            threshold=threshold,
            hit=hit,
            reroll_of=reroll_of,
            hit_group=self._hit_group(unit),
        )
        return shot, hit

    def _modified_combat_factor(
        self, side_key: SideKey, unit: UnitState, round_name: RoundName
    ) -> int:
        base = unit.source.attack if side_key == "attacker" else unit.source.defense
        value = base
        value += self._leader_combat_bonus(side_key)
        value += self._terrain_combat_modifier(side_key)
        value += self._round_modifier(round_name)
        value += self._side_modifier(side_key, unit, round_name)
        if side_key == "attacker" and self.battle.battle.defender_entrenched:
            value -= 1
        if side_key == "defender" and self.first_combat_round:
            value += self.battle.battle.connection_defender_modifier
        if self._has_armor_superiority(side_key):
            value += 1
        return value

    def _side_modifier(self, side_key: SideKey, unit: UnitState, round_name: RoundName) -> int:
        side = self.sides[side_key].source
        total = 0
        for modifier in side.boosters + side.modifiers:
            if modifier.rounds and round_name not in modifier.rounds:
                continue
            if modifier.tags and unit.tags.isdisjoint(set(modifier.tags)):
                continue
            total += modifier.combat
            total += modifier.attack if side_key == "attacker" else modifier.defense
        return total

    def _leader_combat_bonus(self, side_key: SideKey) -> int:
        own = self.sides[side_key].source.leader.combat if self.sides[side_key].source.leader else 0
        other_key = OPPONENT[side_key]
        other = (
            self.sides[other_key].source.leader.combat
            if self.sides[other_key].source.leader
            else 0
        )
        return max(0, own - other)

    def _terrain_combat_modifier(self, side_key: SideKey) -> int:
        return (
            self.battle.battle.attacker_combat_modifier
            if side_key == "attacker"
            else self.battle.battle.defender_combat_modifier
        )

    def _round_modifier(self, round_name: RoundName) -> int:
        if round_name == "artillery":
            return self.battle.battle.artillery_modifier
        if round_name == "air_support":
            return self.battle.battle.air_modifier
        if round_name == "mines":
            return self.battle.battle.mine_modifier
        if round_name == "recon":
            return self.battle.battle.recon_modifier
        return 0

    def _allocate_hits(
        self,
        target_key: SideKey,
        hits_by_group: dict[str, int],
        include_panicked: bool = False,
    ) -> tuple[dict[str, int], int]:
        allocations: dict[str, int] = {}
        wasted = 0

        cav_hits = hits_by_group.get("cav", 0)
        if cav_hits:
            remaining = self._distribute_to_group(target_key, True, cav_hits, allocations, include_panicked)
            if remaining:
                remaining = self._distribute_to_group(
                    target_key, False, remaining, allocations, include_panicked
                )
            wasted += remaining

        other_hits = hits_by_group.get("other", 0)
        if other_hits:
            remaining = self._distribute_to_group(
                target_key, False, other_hits, allocations, include_panicked
            )
            if remaining:
                assignable_to_cav = remaining // 2
                wasted += remaining - assignable_to_cav
                remaining = self._distribute_to_group(
                    target_key, True, assignable_to_cav, allocations, include_panicked
                )
                wasted += remaining

        return allocations, wasted

    def _distribute_to_group(
        self,
        target_key: SideKey,
        cav_group: bool,
        hits: int,
        allocations: dict[str, int],
        include_panicked: bool,
    ) -> int:
        remaining = hits
        priorities = (LossPriority.first, LossPriority.normal, LossPriority.last)
        for priority in priorities:
            candidates = [
                unit
                for unit in self._targetable_units(target_key, include_panicked)
                if self._is_cav_unit(unit) == cav_group and unit.source.loss_priority == priority
            ]
            remaining = self._distribute_proportionally(candidates, remaining, allocations)
            if remaining <= 0:
                return 0
        return remaining

    def _distribute_proportionally(
        self,
        candidates: list[UnitState],
        hits: int,
        allocations: dict[str, int],
    ) -> int:
        remaining = hits
        while remaining > 0:
            available = [
                unit
                for unit in candidates
                if unit.strength - allocations.get(unit.id, 0) > 0
            ]
            if not available:
                return remaining
            capacity = {
                unit.id: unit.strength - allocations.get(unit.id, 0)
                for unit in available
            }
            batch = min(remaining, sum(capacity.values()))
            total_capacity = sum(capacity.values())
            shares: dict[str, int] = {}
            remainders: list[tuple[float, int, UnitState]] = []
            for position, unit in enumerate(available):
                exact = batch * capacity[unit.id] / total_capacity
                share = min(floor(exact), capacity[unit.id])
                shares[unit.id] = share
                remainders.append((exact - share, -position, unit))

            assigned = sum(shares.values())
            for _, _, unit in sorted(remainders, reverse=True):
                if assigned >= batch:
                    break
                if shares[unit.id] < capacity[unit.id]:
                    shares[unit.id] += 1
                    assigned += 1

            if assigned == 0:
                return remaining

            for unit_id, amount in shares.items():
                if amount:
                    allocations[unit_id] = allocations.get(unit_id, 0) + amount
            remaining -= assigned
        return 0

    def _apply_hits(
        self,
        applied_hits_by_unit: dict[SideKey, dict[str, int]],
        start_strengths: dict[SideKey, dict[str, int]],
        events: list[str],
        round_name: RoundName,
    ) -> None:
        for side_key, hits_by_unit in applied_hits_by_unit.items():
            side = self.sides[side_key]
            for unit_id, hits in hits_by_unit.items():
                unit = self._unit_by_id(side_key, unit_id)
                actual = min(hits, unit.strength)
                unit.strength -= actual
                if actual:
                    events.append(
                        f"{self._side_name(side_key)} {unit.name} takes {actual} hit(s)."
                    )
                if unit.strength <= 0 and not unit.destroyed:
                    unit.destroyed = True
                    unit.panicked = False
                    side.losses_count += 1
                    side.current_bm -= 1
                    events.append(
                        f"{self._side_name(side_key)} {unit.name} is eliminated; BM -1."
                    )

    def _apply_panic_checks(
        self,
        applied_hits_by_unit: dict[SideKey, dict[str, int]],
        start_strengths: dict[SideKey, dict[str, int]],
        events: list[str],
    ) -> None:
        for side_key, hits_by_unit in applied_hits_by_unit.items():
            side = self.sides[side_key]
            for unit_id, hits in hits_by_unit.items():
                unit = self._unit_by_id(side_key, unit_id)
                if unit.destroyed or unit.panicked:
                    continue
                start_strength = start_strengths[side_key].get(unit_id, 0)
                if not start_strength or hits < ceil(start_strength / 2):
                    continue
                roll = self.rng.randint(0, 9)
                threshold = unit.source.morale * 2
                if roll > threshold:
                    unit.panicked = True
                    side.panic_count += 1
                    side.current_bm -= 1
                    events.append(
                        f"{self._side_name(side_key)} {unit.name} panics "
                        f"(roll {roll} > {threshold}); BM -1."
                    )
                else:
                    events.append(
                        f"{self._side_name(side_key)} {unit.name} holds cohesion "
                        f"(panic roll {roll} <= {threshold})."
                    )

    def _apply_heavy_loss_checks(
        self,
        start_totals: dict[SideKey, int],
        start_strengths: dict[SideKey, dict[str, int]],
        events: list[str],
    ) -> None:
        for side_key in SIDE_KEYS:
            if start_totals[side_key] <= 0:
                continue
            current_total = sum(
                self._unit_by_id(side_key, unit_id).strength
                for unit_id in start_strengths[side_key]
            )
            lost = start_totals[side_key] - current_total
            if lost > start_totals[side_key] / 2:
                self.sides[side_key].current_bm -= 1
                events.append(
                    f"{self._side_name(side_key)} suffers heavy losses ({lost}/"
                    f"{start_totals[side_key]} SP); BM -1."
                )

    def _check_end_after_round(self, report: RoundReport) -> None:
        active = {key: len(self._active_combat_units(key)) for key in SIDE_KEYS}
        if active["attacker"] == 0 or active["defender"] == 0:
            self.finished_reason = "one side has no combat units left on the battlefield"
            return

        demoralized = [key for key in SIDE_KEYS if self.sides[key].current_bm <= 0]
        if not demoralized:
            return

        test_side: SideKey | None
        if len(demoralized) == 1:
            test_side = demoralized[0]
        else:
            attacker_score = self.sides["attacker"].losses_count + self.sides["attacker"].panic_count
            defender_score = self.sides["defender"].losses_count + self.sides["defender"].panic_count
            if attacker_score != defender_score:
                test_side = "attacker" if attacker_score > defender_score else "defender"
            elif self.sides["attacker"].panic_count != self.sides["defender"].panic_count:
                test_side = (
                    "attacker"
                    if self.sides["attacker"].panic_count > self.sides["defender"].panic_count
                    else "defender"
                )
            else:
                test_side = None
                report.events.append("Both sides are demoralized equally; no rout test is made.")

        if test_side:
            self._rout_test(test_side, report.events)

    def _rout_test(self, side_key: SideKey, events: list[str]) -> None:
        side = self.sides[side_key]
        roll = self.rng.randint(0, 9)
        passed = roll == 0 or roll <= side.current_bm
        if passed:
            events.append(
                f"{self._side_name(side_key)} passes rout test "
                f"(roll {roll}, BM {side.current_bm})."
            )
            return
        side.routed = True
        self.routed_side = side_key
        self.finished_reason = f"{self._side_name(side_key)} fails rout test"
        events.append(
            f"{self._side_name(side_key)} routs (roll {roll}, BM {side.current_bm})."
        )

    def _apply_next_round_exhaustion(self, next_number: int) -> list[str]:
        events: list[str] = []
        for side_key in SIDE_KEYS:
            self.sides[side_key].current_bm -= 1
            events.append(
                f"Next {next_number} battle exhaustion: {self._side_name(side_key)} BM -1."
            )
        return events

    def _maybe_retreat_before_next(self, next_number: int, events: list[str]) -> bool:
        for side_key in SIDE_KEYS:
            policy = self.sides[side_key].source.retreat_policy
            should_retreat = policy.mode == "after_main" or (
                policy.mode == "when_bm_non_positive" and self.sides[side_key].current_bm <= 0
            )
            if should_retreat:
                self.sides[side_key].retreated = True
                self.retreated_side = side_key
                self.finished_reason = f"{self._side_name(side_key)} voluntarily retreats"
                events.append(
                    f"{self._side_name(side_key)} retreats before Next {next_number}; pursuit prevented."
                )
                return True
        return False

    def _should_run_pursuit(self) -> bool:
        if not self.routed_side or not self.battle.battle.pursuit_allowed:
            return False
        if self.retreated_side and self.sides[self.retreated_side].source.retreat_policy.prevent_pursuit:
            return False
        return bool(self._shooters(self._winner_key(), "pursuit"))

    def _apply_total_elimination(self) -> list[str]:
        events: list[str] = []
        for side_key in SIDE_KEYS:
            combat_units = [unit for unit in self.sides[side_key].units if unit.source.role == UnitRole.combat]
            if not combat_units or not all(unit.destroyed for unit in combat_units):
                continue
            support_units = [
                unit
                for unit in self.sides[side_key].units
                if unit.source.role == UnitRole.support and not unit.destroyed and unit.strength > 0
            ]
            eliminated = len(support_units) // 2
            for unit in support_units[:eliminated]:
                unit.strength = 0
                unit.destroyed = True
                events.append(
                    f"Total elimination removes support unit {self._side_name(side_key)} {unit.name}."
                )
        return events

    def _final_report(self) -> FinalReport:
        winner_key = self._winner_key()
        loser_key = OPPONENT[winner_key]
        return FinalReport(
            winner=self._side_name(winner_key),
            winner_key=winner_key,
            loser=self._side_name(loser_key),
            loser_key=loser_key,
            reason=self.finished_reason or "battle resolved",
            routed_side=self.routed_side,
            retreated_side=self.retreated_side,
            pursuit_happened=self.pursuit_happened,
            breakthrough_available=self._breakthrough_available(winner_key),
        )

    def _winner_key(self) -> SideKey:
        active = {key: len(self._active_combat_units(key)) for key in SIDE_KEYS}
        if active["attacker"] > 0 and active["defender"] == 0:
            return "attacker"
        if active["defender"] > 0 and active["attacker"] == 0:
            return "defender"
        if self.retreated_side:
            return OPPONENT[self.retreated_side]
        if self.routed_side:
            return OPPONENT[self.routed_side]
        return "defender"

    def _breakthrough_available(self, winner_key: SideKey) -> bool:
        if winner_key != "attacker" or not self.battle.battle.breakthrough_allowed:
            return False
        return any(self._is_pursuit_capable(unit) for unit in self._active_units(winner_key))

    def _battle_finished(self) -> bool:
        return bool(self.finished_reason or self.routed_side or self.retreated_side)

    def _round_has_shooters(self, round_name: RoundName) -> bool:
        return any(self._shooters(side_key, round_name) for side_key in SIDE_KEYS)

    def _shooters(self, side_key: SideKey, round_name: RoundName) -> list[UnitState]:
        units = self._active_units(side_key)
        if round_name == "artillery":
            return [unit for unit in units if "artillery" in unit.tags]
        if round_name == "air_support":
            return [unit for unit in units if self._is_air_support_unit(unit)]
        if round_name == "mines":
            return [unit for unit in units if "mine" in unit.tags or "minefield" in unit.tags]
        if round_name == "recon":
            return [unit for unit in units if "recon" in unit.tags or "reconnaissance" in unit.tags]
        if round_name in {"main", "next"}:
            return [
                unit
                for unit in units
                if unit.source.role == UnitRole.combat
                and (unit.source.domain != UnitDomain.air or not unit.tags.isdisjoint(MAIN_AIR_TAGS))
            ]
        if round_name == "pursuit":
            return [unit for unit in units if self._is_pursuit_capable(unit)]
        return []

    def _active_units(self, side_key: SideKey) -> list[UnitState]:
        return [
            unit
            for unit in self.sides[side_key].units
            if unit.strength > 0 and not unit.destroyed and not unit.panicked
        ]

    def _active_combat_units(self, side_key: SideKey) -> list[UnitState]:
        return [
            unit
            for unit in self._active_units(side_key)
            if unit.source.role == UnitRole.combat
        ]

    def _targetable_units(self, side_key: SideKey, include_panicked: bool) -> list[UnitState]:
        return [
            unit
            for unit in self.sides[side_key].units
            if unit.strength > 0
            and not unit.destroyed
            and (include_panicked or not unit.panicked)
        ]

    def _start_strengths(self, include_panicked: bool) -> dict[SideKey, dict[str, int]]:
        return {
            key: {
                unit.id: unit.strength
                for unit in self._targetable_units(key, include_panicked)
            }
            for key in SIDE_KEYS
        }

    def _unit_by_id(self, side_key: SideKey, unit_id: str) -> UnitState:
        for unit in self.sides[side_key].units:
            if unit.id == unit_id:
                return unit
        raise KeyError(f"unknown unit id {unit_id!r} for {side_key}")

    def _snapshots_by_side(self) -> dict[SideKey, list[UnitSnapshot]]:
        return {
            key: [unit.snapshot() for unit in self.sides[key].units]
            for key in SIDE_KEYS
        }

    def _empty_round(
        self, name: RoundName, index: int, label: str, events: list[str]
    ) -> RoundReport:
        return RoundReport(
            name=name,
            label=label,
            index=index,
            events=events,
            shots=[],
            hits_inflicted={"attacker": {"cav": 0, "other": 0}, "defender": {"cav": 0, "other": 0}},
            hits_taken={"attacker": 0, "defender": 0},
            morale={key: self.sides[key].current_bm for key in SIDE_KEYS},
            units=self._snapshots_by_side(),
        )

    def _round_label(self, round_name: RoundName) -> str:
        return {
            "artillery": "Artillery Preparation",
            "air_support": "Air Support",
            "mines": "Mines",
            "recon": "Recon",
            "main": "Main",
            "pursuit": "Pursuit",
            "setup": "Setup",
            "next": "Next",
        }[round_name]

    def _side_name(self, side_key: SideKey) -> str:
        return self.sides[side_key].source.name

    def _hit_group(self, unit: UnitState) -> str:
        return "cav" if self._is_cav_unit(unit) else "other"

    def _is_cav_unit(self, unit: UnitState) -> bool:
        return not unit.tags.isdisjoint(CAV_TAGS)

    def _is_armor_unit(self, unit: UnitState) -> bool:
        return bool(unit.tags.intersection({"armor", "armour", "tank"}))

    def _is_air_unit(self, unit: UnitState) -> bool:
        return unit.source.domain == UnitDomain.air or "air" in unit.tags

    def _is_air_support_unit(self, unit: UnitState) -> bool:
        return unit.source.domain == UnitDomain.air and not unit.tags.isdisjoint(AIR_SUPPORT_TAGS)

    def _is_pursuit_capable(self, unit: UnitState) -> bool:
        return not unit.tags.isdisjoint(PURSUIT_TAGS)

    def _has_armor_superiority(self, side_key: SideKey) -> bool:
        if not self.battle.battle.armor_superiority_allowed:
            return False
        own = sum(1 for unit in self._active_units(side_key) if self._is_armor_unit(unit))
        other = sum(1 for unit in self._active_units(OPPONENT[side_key]) if self._is_armor_unit(unit))
        return own >= 2 and own >= max(1, other * 2)


def round_half_up(value: float) -> int:
    return int(floor(value + 0.5))
