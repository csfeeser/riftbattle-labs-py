from dataclasses import dataclass


@dataclass
class StatModifier:
    """A temporary stat boost."""

    stat_name: str
    bonus: int
    duration: int


def clamp(value: int, minimum: int, maximum: int) -> int:
    """Return value bounded by minimum and maximum."""
    if value < minimum:
        return minimum
    if value > maximum:
        return maximum
    return value


class FighterStatsMixin:
    """Stat-related methods for Fighter (kept in this file to mirror the Go layout)."""

    def apply_modifier(self, modifier: StatModifier) -> None:
        """Add a temporary stat bonus."""
        if modifier.stat_name == "power":
            self.stats.power += modifier.bonus
        elif modifier.stat_name == "defense":
            self.stats.defense += modifier.bonus
        elif modifier.stat_name == "agility":
            self.stats.agility += modifier.bonus
        elif modifier.stat_name == "spirit":
            self.stats.spirit += modifier.bonus
        elif modifier.stat_name == "crit":
            self.stats.crit_chance += modifier.bonus

    def tick_modifiers(self) -> None:
        """Decrement stat modifier durations."""
        # This will be expanded when modifiers are stored

    def calculate_stat_bonus(self):
        """Calculate the total stat bonus from equipment and effects."""
        from fighters.fighter import Stats

        bonus = Stats(0, 0, 0, 0, 0)

        # Equipment bonuses would be calculated here
        # Tight coupling issue: game.py directly accesses Fighter.stats
        # Should be abstracted away

        return bonus

    def get_stat_by_name(self, stat_name: str) -> int:
        """Get a stat value by name."""
        if stat_name == "power":
            return self.stats.power
        if stat_name == "defense":
            return self.stats.defense
        if stat_name == "agility":
            return self.stats.agility
        if stat_name == "spirit":
            return self.stats.spirit
        if stat_name == "crit":
            return self.stats.crit_chance
        return 0

    def adjust_health(self, amount: int) -> int:
        """Adjust the fighter's HP and return the change."""
        before = self.hp
        self.hp = clamp(self.hp + amount, 0, self.max_hp)
        return self.hp - before

    def restore_mana(self, amount: int) -> int:
        """Restore MP and return the change."""
        before = self.mp
        self.mp = clamp(self.mp + amount, 0, self.max_mp)
        return self.mp - before
