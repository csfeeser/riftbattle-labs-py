from dataclasses import dataclass, field

from fighters.fighter import Fighter


@dataclass
class SkillDefinition:
    """Defines when a skill unlocks."""

    name: str
    unlocks_at_level: int
    mana_cost: int
    power_bonus: int


def default_skill_tree() -> dict[str, SkillDefinition]:
    """Return the standard skill progression."""
    return {
        "power_strike": SkillDefinition(
            name="Power Strike", unlocks_at_level=5, mana_cost=10, power_bonus=8
        ),
        "defensive_stance": SkillDefinition(
            name="Defensive Stance", unlocks_at_level=10, mana_cost=5, power_bonus=0
        ),
        "dual_strike": SkillDefinition(
            name="Dual Strike", unlocks_at_level=15, mana_cost=15, power_bonus=12
        ),
        "heal": SkillDefinition(name="Heal", unlocks_at_level=3, mana_cost=20, power_bonus=0),
    }


@dataclass
class ProgressionTracker:
    """Tracks a fighter's leveling progression."""

    fighter: Fighter
    xp_multiplier: float = 1.0
    skill_tree: dict[str, SkillDefinition] = field(default_factory=default_skill_tree)

    def recalculate_unlocked_skills(self) -> None:
        """Update which skills should be unlocked at current level."""
        self.fighter.skills_unlocked = ["attack"]

        for skill_name, skill_def in self.skill_tree.items():
            if self.fighter.level >= skill_def.unlocks_at_level:
                if not self.fighter.has_skill(skill_name):
                    self.fighter.skills_unlocked.append(skill_name)

    def gain_xp(self, base_xp: int) -> None:
        """Apply experience gain with multipliers."""
        xp_gain = int(float(base_xp) * self.xp_multiplier)
        self.fighter.add_xp(xp_gain)
        self.recalculate_unlocked_skills()

    def set_xp_multiplier(self, multiplier: float) -> None:
        """Set the multiplier for XP gains (for training mode, etc)."""
        self.xp_multiplier = multiplier

    def get_xp_to_next_level(self) -> int:
        """Return how much XP is needed to level up."""
        xp_per_level = 100
        return xp_per_level - self.fighter.xp

    def prestige_reset(self) -> None:
        """Reset the fighter to level 1 with bonus stats (advanced mechanic)."""
        old_level = self.fighter.level

        # Add prestige bonus
        bonus_per_level = old_level // 5
        self.fighter.base_stats.power += bonus_per_level
        self.fighter.base_stats.defense += bonus_per_level // 2
        self.fighter.base_stats.agility += bonus_per_level // 2
        self.fighter.base_stats.spirit += bonus_per_level

        # Reset level and XP
        self.fighter.level = 1
        self.fighter.xp = 0

        # Recalculate unlocked skills
        self.recalculate_unlocked_skills()

    def get_level_progress(self) -> float:
        """Return progress to next level as a percentage."""
        xp_required = 100 + (self.fighter.level * 50)
        return float(self.fighter.xp) / float(xp_required) * 100
