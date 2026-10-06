from dataclasses import dataclass

from equipment.equipment import (
    RARITY_COMMON,
    RARITY_EPIC,
    RARITY_LEGENDARY,
    RARITY_RARE,
    RARITY_UNCOMMON,
)


@dataclass
class RarityBonus:
    """Stat bonuses granted by equipment rarity."""

    rarity: str
    power_bonus: float
    defense_bonus: float
    agility_bonus: float
    spirit_bonus: float
    crit_bonus: int
    luck_bonus: int


def get_rarity_bonus(rarity: str) -> RarityBonus:
    """Return the bonus multiplier for a rarity level."""
    bonuses = {
        RARITY_COMMON: RarityBonus(RARITY_COMMON, 1.0, 1.0, 1.0, 1.0, 0, 0),
        RARITY_UNCOMMON: RarityBonus(RARITY_UNCOMMON, 1.15, 1.15, 1.10, 1.10, 2, 1),
        RARITY_RARE: RarityBonus(RARITY_RARE, 1.35, 1.35, 1.30, 1.30, 5, 3),
        RARITY_EPIC: RarityBonus(RARITY_EPIC, 1.6, 1.6, 1.5, 1.5, 10, 5),
        RARITY_LEGENDARY: RarityBonus(RARITY_LEGENDARY, 2.0, 2.0, 2.0, 2.0, 15, 10),
    }

    if rarity in bonuses:
        return bonuses[rarity]

    return bonuses[RARITY_COMMON]


def apply_rarity_bonus(base_value: int, rarity: str, bonus_type: str) -> int:
    """Apply rarity bonuses to a base value."""
    rarity_bonus = get_rarity_bonus(rarity)

    if bonus_type == "power":
        return int(float(base_value) * rarity_bonus.power_bonus)
    if bonus_type == "defense":
        return int(float(base_value) * rarity_bonus.defense_bonus)
    if bonus_type == "agility":
        return int(float(base_value) * rarity_bonus.agility_bonus)
    if bonus_type == "spirit":
        return int(float(base_value) * rarity_bonus.spirit_bonus)
    return base_value
