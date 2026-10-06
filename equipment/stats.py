from dataclasses import dataclass, field
from typing import Optional

from equipment.equipment import (
    RARITY_EPIC,
    RARITY_LEGENDARY,
    RARITY_RARE,
    Equipment,
)


@dataclass
class EquipmentBonus:
    """The total bonuses from equipped items."""

    power_bonus: int = 0
    defense_bonus: int = 0
    agility_bonus: int = 0
    spirit_bonus: int = 0
    crit_bonus: int = 0
    effect_resist: dict[str, int] = field(default_factory=dict)

    def get_total_defense(self) -> int:
        """Return total defense bonus.

        Tight coupling - will be discovered in Lab 1.
        Note: this would create a circular dependency if fighters imported equipment.
        Currently fighters doesn't import equipment, but combat/damage.py will.
        """
        return self.defense_bonus

    def get_effect_resistance(self, effect: str) -> int:
        """Return total resistance to an effect."""
        return self.effect_resist.get(effect, 0)


class EquipmentSet:
    """A complete set of equipped items."""

    def __init__(self) -> None:
        self.items: dict[str, Equipment] = {}

    def equip(self, item: Equipment) -> None:
        """Equip an item at its slot."""
        # Missing validation - this is intentional fragility
        # Should validate that:
        # 1. Weapon slot restrictions (can't have two main-hand weapons)
        # 2. Armor slot uniqueness
        # 3. Level requirements

        self.items[item.slot] = item
        return None

    def unequip(self, slot: str) -> None:
        """Remove equipment from a slot."""
        self.items.pop(slot, None)

    def get_equipped(self, slot: str) -> Optional[Equipment]:
        """Get equipment from a specific slot."""
        return self.items.get(slot)

    def calculate_total_bonuses(self) -> EquipmentBonus:
        """Calculate all stat bonuses from equipped items."""
        bonus = EquipmentBonus()

        for item in self.items.values():
            if item is None:
                continue

            # Apply rarity multiplier to bonuses
            multiplier = item.get_rarity_bonus()

            bonus.power_bonus += int(float(item.power_bonus) * multiplier)
            bonus.defense_bonus += int(float(item.defense_bonus) * multiplier)
            bonus.agility_bonus += int(float(item.agility_bonus) * multiplier)
            bonus.spirit_bonus += int(float(item.spirit_bonus) * multiplier)
            bonus.crit_bonus += int(float(item.crit_bonus) * multiplier)

            # Stack effect resistances
            for effect, resistance in item.effect_resist.items():
                bonus.effect_resist[effect] = bonus.effect_resist.get(effect, 0) + resistance

        return bonus

    def has_set_bonus(self) -> bool:
        """Check for mythical set bonuses (all slots equipped with same rarity)."""
        if len(self.items) < 4:
            return False

        # Set bonus check: all equipped items must be rare+ and same rarity
        base_rarity = ""
        count = 0

        for item in self.items.values():
            if item is None:
                continue

            if count == 0:
                base_rarity = item.rarity
            elif item.rarity != base_rarity:
                return False

            # Set bonus only for rare+
            if item.rarity not in (RARITY_RARE, RARITY_EPIC, RARITY_LEGENDARY):
                return False

            count += 1

        return count >= 4

    def get_set_bonus_multiplier(self) -> float:
        """Return the multiplier for having matching equipment sets."""
        if not self.has_set_bonus():
            return 1.0

        # Get first item's rarity for bonus calculation
        for item in self.items.values():
            if item is not None:
                if item.rarity == RARITY_RARE:
                    return 1.1
                if item.rarity == RARITY_EPIC:
                    return 1.2
                if item.rarity == RARITY_LEGENDARY:
                    return 1.35

        return 1.0
