from __future__ import annotations

from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


SideKey = Literal["attacker", "defender"]
RoundName = Literal[
    "setup",
    "artillery",
    "air_support",
    "mines",
    "recon",
    "main",
    "next",
    "pursuit",
]


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class UnitRole(str, Enum):
    combat = "combat"
    support = "support"


class UnitDomain(str, Enum):
    land = "land"
    air = "air"
    sea = "sea"


class LossPriority(str, Enum):
    first = "first"
    normal = "normal"
    last = "last"


class RetreatMode(str, Enum):
    never = "never"
    after_main = "after_main"
    when_bm_non_positive = "when_bm_non_positive"


class ModifierInput(StrictModel):
    name: str = Field(min_length=1)
    combat: int = 0
    attack: int = 0
    defense: int = 0
    morale: int = 0
    rounds: list[RoundName] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)

    @field_validator("tags", mode="before")
    @classmethod
    def normalize_tags(cls, value: Any) -> list[str]:
        if value is None:
            return []
        return [str(tag).strip().lower() for tag in value if str(tag).strip()]


class LeaderInput(StrictModel):
    name: str = Field(min_length=1)
    combat: int = Field(default=0, ge=0, le=9)
    morale: int = Field(default=0, ge=0, le=9)


class RetreatPolicyInput(StrictModel):
    mode: RetreatMode = RetreatMode.never
    prevent_pursuit: bool = True


class UnitInput(StrictModel):
    id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    role: UnitRole = UnitRole.combat
    domain: UnitDomain = UnitDomain.land
    attack: int = Field(default=0, ge=0, le=9)
    defense: int = Field(default=0, ge=0, le=9)
    morale: int = Field(default=1, ge=0, le=9)
    strength: int = Field(default=1, ge=0)
    max_strength: int = Field(default=1, ge=1)
    rof: int = Field(default=1, ge=1, le=5)
    tags: list[str] = Field(default_factory=list)
    loss_priority: LossPriority = LossPriority.normal

    @field_validator("tags", mode="before")
    @classmethod
    def normalize_tags(cls, value: Any) -> list[str]:
        if value is None:
            return []
        return [str(tag).strip().lower() for tag in value if str(tag).strip()]

    @model_validator(mode="after")
    def validate_strength(self) -> "UnitInput":
        if self.strength > self.max_strength:
            raise ValueError("strength cannot exceed max_strength")
        return self


class SideInput(StrictModel):
    name: str = Field(min_length=1)
    leader: LeaderInput | None = None
    scenario_morale_bonus: int = 0
    boosters: list[ModifierInput] = Field(default_factory=list)
    modifiers: list[ModifierInput] = Field(default_factory=list)
    retreat_policy: RetreatPolicyInput = Field(default_factory=RetreatPolicyInput)
    units: list[UnitInput] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_unit_ids(self) -> "SideInput":
        ids = [unit.id for unit in self.units]
        if len(ids) != len(set(ids)):
            raise ValueError("unit ids must be unique within a side")
        if not any(unit.role == UnitRole.combat and unit.strength > 0 for unit in self.units):
            raise ValueError("side must include at least one surviving combat unit")
        return self


class BattleMetaInput(StrictModel):
    scenario_name: str = "Untitled SGS Scenario"
    turn_number: int = Field(default=1, ge=1)
    date_label: str = "Turn 1"
    active_side: str = "Attacker"
    phase: str = "Battles"
    seed: int = 1


class BattleSettingsInput(StrictModel):
    region: str = Field(default="Battle Region", min_length=1)
    terrain: str = "Clear"
    attacker_combat_modifier: int = 0
    defender_combat_modifier: int = 0
    attacker_morale_modifier: int = 0
    defender_morale_modifier: int = 0
    air_modifier: int = 0
    artillery_modifier: int = 0
    mine_modifier: int = 0
    recon_modifier: int = 0
    connection_defender_modifier: int = 0
    defender_entrenched: bool = False
    recon_allowed: bool = True
    pursuit_allowed: bool = True
    breakthrough_allowed: bool = True
    armor_superiority_allowed: bool = True
    max_next_rounds: int = Field(default=3, ge=0, le=3)
    non_simultaneous_side: SideKey | None = None


class BattleInput(StrictModel):
    meta: BattleMetaInput = Field(default_factory=BattleMetaInput)
    battle: BattleSettingsInput = Field(default_factory=BattleSettingsInput)
    attacker: SideInput
    defender: SideInput


class MoraleBreakdown(StrictModel):
    total: int
    average_combat_morale: int
    leader_morale: int
    terrain: int
    scenario: int
    air_presence: int
    armor_presence: int
    armor_superiority: int
    modifiers: int


class ShotRoll(StrictModel):
    side: SideKey
    unit_id: str
    unit_name: str
    round: RoundName
    shot_number: int
    roll: int
    modified_factor: int
    threshold: int
    hit: bool
    reroll_of: int | None = None
    hit_group: Literal["cav", "other"]


class UnitSnapshot(StrictModel):
    id: str
    name: str
    side: SideKey
    role: UnitRole
    domain: UnitDomain
    strength: int
    max_strength: int
    morale: int
    tags: list[str]
    loss_priority: LossPriority
    destroyed: bool
    panicked: bool


class RoundReport(StrictModel):
    name: RoundName
    label: str
    index: int
    events: list[str] = Field(default_factory=list)
    shots: list[ShotRoll] = Field(default_factory=list)
    hits_inflicted: dict[SideKey, dict[str, int]]
    hits_taken: dict[SideKey, int]
    morale: dict[SideKey, int]
    units: dict[SideKey, list[UnitSnapshot]]


class FinalReport(StrictModel):
    winner: str
    winner_key: SideKey
    loser: str
    loser_key: SideKey
    reason: str
    routed_side: SideKey | None = None
    retreated_side: SideKey | None = None
    pursuit_happened: bool = False
    breakthrough_available: bool = False


class SimulationReport(StrictModel):
    meta: BattleMetaInput
    battle: BattleSettingsInput
    initial_battle_morale: dict[SideKey, MoraleBreakdown]
    rounds: list[RoundReport]
    final: FinalReport
    survivors: dict[SideKey, list[UnitSnapshot]]
