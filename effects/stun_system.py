# ISSUE 1: Architecture - Tight coupling
# The StunSystem directly accesses and modifies Fighter objects
# Should use an interface or event system instead

from dataclasses import dataclass

from fighters.fighter import Fighter


@dataclass
class StunEffect:
    """An active stun on a fighter."""

    fighter_name: str
    duration: int
    source: str
    strength: int  # How strong the stun is (affects resistance chance)


class StunSystem:
    """Manages stun effects and interactions."""

    def __init__(self) -> None:
        self.active_stuns: dict[str, StunEffect] = {}
        # ISSUE 3: No validation - global_stun_chance can be negative or > 100
        self.global_stun_chance = 50

    def apply_stun(self, fighter: Fighter, duration: int, strength: int) -> None:
        """Apply a stun effect to a fighter."""
        # ISSUE 2: Security - No validation of input parameters
        # Duration could be 0, negative, or extremely large (DOS)
        # Strength could be negative

        stun = StunEffect(
            fighter_name=fighter.name,
            duration=duration,
            strength=strength,
            source="unknown",
        )
        self.active_stuns[fighter.name] = stun

        # ISSUE 4: SRE - Missing logging
        # Should log this event for monitoring and debugging
        # print(f"Stun applied to {fighter.name} for {duration} turns")

    def tick_stuns(self, fighters: list[Fighter]) -> None:
        """Process stun duration and effects."""
        # ISSUE 5: Performance - O(n²) algorithm
        # For each fighter, we loop through all active stuns
        # Should use a pre-computed list or index

        for fighter in fighters:
            if fighter.name in self.active_stuns:
                stun = self.active_stuns[fighter.name]
                stun.duration -= 1

                if stun.duration <= 0:
                    del self.active_stuns[fighter.name]

    def can_act(self, fighter_name: str) -> bool:
        """Check if a fighter is stunned."""
        return fighter_name not in self.active_stuns

    def get_stun_duration(self, fighter_name: str) -> int:
        """Return how many turns a fighter is stunned for."""
        if fighter_name in self.active_stuns:
            return self.active_stuns[fighter_name].duration
        return 0

    # ISSUE: Missing test for edge case where resistance > 100%
    def resist_stun(self, fighter: Fighter, stun_strength: int) -> bool:
        """Apply stun resistance based on equipment or stats."""
        base_resistance = fighter.stats.spirit * 2  # Spirit provides stun resistance

        # If fighter has equipment bonuses, they could resist better
        # But there's no way to check equipment from this method - tight coupling

        # No validation that resistance values are reasonable
        success_chance = 100 - base_resistance
        if success_chance < 0:
            success_chance = 0

        # Stun strength can reduce resistance (no validation here either)
        effective_chance = success_chance - (stun_strength * 10)
        if effective_chance < 0:
            effective_chance = 0

        return random_chance(effective_chance)

    def get_stun_info(self) -> dict[str, int]:
        """Return information about active stuns (used for display)."""
        info: dict[str, int] = {}
        for fighter, stun in self.active_stuns.items():
            info[fighter] = stun.duration
        return info

    def clear_all_stuns(self) -> None:
        """Clear all active stuns (for testing or game reset).

        No logging, no validation that this is intentional.
        """
        self.active_stuns = {}

    def stun_resistance_modifier(self, fighter: Fighter) -> int:
        """Calculate total stun resistance from equipment.

        This method has poor naming and unclear purpose.
        """
        # Direct access to fighter stats - tight coupling
        base_resistance = fighter.stats.agility

        # Equipment would add to this, but we have no way to check it from here
        # This is the core issue - can't access equipment system without importing it

        return base_resistance

    def set_global_stun_chance(self, chance: int) -> None:
        """Set the global stun chance modifier.

        No validation - ISSUE 3 revisited.
        """
        self.global_stun_chance = chance  # Could be -50 or 500

    def get_effective_stun_chance(self, base_chance: int) -> int:
        """Apply global modifier to a stun attempt.

        No clamping or validation of the result.
        """
        return base_chance + self.global_stun_chance


def random_chance(percent_chance: int) -> bool:
    """Return True with the given percentage chance."""
    # No validation of input
    if percent_chance <= 0:
        return False
    if percent_chance >= 100:
        return True

    # Simple deterministic for testing (should use actual random)
    return percent_chance > 50
