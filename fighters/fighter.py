from dataclasses import dataclass, field, replace
from datetime import datetime
from typing import Any, Optional

from fighters.stats import FighterStatsMixin

SLOT_MAIN_HAND = "main_hand"
SLOT_OFF_HAND = "off_hand"
SLOT_HEAD = "head"
SLOT_CHEST = "chest"
SLOT_LEGS = "legs"
SLOT_FEET = "feet"
SLOT_ACCESSORY = "accessory"


@dataclass
class Stats:
    """A fighter's core attributes."""

    power: int
    defense: int
    agility: int
    spirit: int
    crit_chance: int


@dataclass
class Fighter(FighterStatsMixin):
    """A combatant in the game."""

    # Identity
    name: str
    fighter_class: str
    id: str = ""

    # Health & Resources
    hp: int = 0
    max_hp: int = 0
    mp: int = 0
    max_mp: int = 0

    # Base attributes
    stats: Stats = field(default_factory=lambda: Stats(0, 0, 0, 0, 0))
    base_stats: Stats = field(default_factory=lambda: Stats(0, 0, 0, 0, 0))

    # Equipment (NEW)
    equipment: dict[str, Any] = field(default_factory=dict)  # Will hold equipment items

    # Combat state
    status: dict[str, int] = field(default_factory=dict)

    # Progression (NEW)
    level: int = 1
    xp: int = 0
    skills_unlocked: list[str] = field(default_factory=list)

    # Inventory (NEW - reference to inventory package)
    inventory_id: str = ""

    # Game state
    training_mode: bool = False
    last_action_time: Optional[datetime] = None

    # Legacy fields for compatibility
    weapon_type: str = ""
    element: str = ""
    armor_type: str = ""

    def add_xp(self, amount: int) -> bool:
        """Add experience points and check for level up."""
        self.xp += amount
        xp_per_level = 100
        if self.xp >= xp_per_level:
            self.level_up()
            return True
        return False

    def level_up(self) -> None:
        """Increase level and stat growth."""
        self.level += 1
        self.base_stats.power += 2
        self.base_stats.defense += 1
        self.base_stats.agility += 1
        self.base_stats.spirit += 2

        # Recalculate effective stats
        self.stats = self.get_effective_stats()

        # Restore health on level up
        self.max_hp += 10
        self.hp = self.max_hp
        self.max_mp = self.stats.spirit * 2
        self.mp = self.max_mp

        # Unlock skills at certain levels
        if self.level == 5:
            self.skills_unlocked.append("power_strike")
        if self.level == 10:
            self.skills_unlocked.append("defensive_stance")

        self.xp = 0

    def get_effective_stats(self) -> Stats:
        """Calculate stats including equipment bonuses."""
        stats = replace(self.base_stats)

        # Equipment bonuses would be applied here
        # For now, just return base stats
        # This will be expanded when equipment package is integrated

        return stats

    def has_skill(self, skill: str) -> bool:
        """Check if the fighter has unlocked a skill."""
        for s in self.skills_unlocked:
            if s == skill:
                return True
        return False

    def can_perform_action(self, action_name: str) -> bool:
        """Check if fighter can perform an action."""
        # Can't act if stunned or defeated
        if self.status.get("stunned", 0) > 0:
            return False
        if self.is_defeated():
            return False

        # Check if skill is unlocked
        if action_name != "attack" and action_name != "defend":
            return self.has_skill(action_name)

        return True

    def is_defeated(self) -> bool:
        """Check if the fighter is defeated."""
        return self.hp <= 0

    def can_act(self) -> bool:
        """Check if the fighter can act this turn."""
        return self.can_perform_action("attack")


def new_fighter(
    name: str,
    fighter_class: str,
    hp: int,
    weapon_type: str,
    element: str,
    armor_type: str,
    stats: Stats,
) -> Fighter:
    """Create a new fighter with the given parameters."""
    max_mp = stats.spirit * 2
    return Fighter(
        name=name,
        fighter_class=fighter_class,
        hp=hp,
        max_hp=hp,
        mp=max_mp,
        max_mp=max_mp,
        stats=replace(stats),
        base_stats=replace(stats),
        status={},
        level=1,
        xp=0,
        skills_unlocked=["attack"],  # Everyone starts with basic attack
        equipment={},
        weapon_type=weapon_type,
        element=element,
        armor_type=armor_type,
    )
