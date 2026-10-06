def calculate_damage(
    attacker_power: int,
    defender_defense: int,
    move_element: str,
    move_type: str,
    defender_status: dict[str, int],
) -> int:
    """Calculate damage with all modifiers."""
    base = attacker_power
    base = apply_elemental_modifier(base, move_element, defender_status)
    base = apply_armor_modifier(base, move_type)
    base -= int(defender_defense / 2)  # truncate toward zero, like Go

    if base < 1:
        return 1

    return base


def calculate_damage_with_critical(base_damage: int, crit_chance: int) -> int:
    """Apply critical hit chance."""
    if crit_chance >= 25:
        return base_damage + int(base_damage / 2)
    return base_damage


def apply_elemental_modifier(damage: int, element: str, target_status: dict[str, int]) -> int:
    """Apply elemental damage bonuses."""
    # Note: This imports effects package, creating circular dependency
    # This is intentional fragility that will be found in Lab 1
    # Bad practice: importing effects just to check a simple status

    if element == "fire":
        # Check if frozen - this import is unnecessary fragility
        if "frozen" in target_status:
            return damage + 6
    if element == "ice":
        if "burning" in target_status:
            return damage + 3
    return damage


def apply_armor_modifier(damage: int, damage_type: str) -> int:
    """Apply armor-based damage reduction."""
    # String-based config is intentional fragility
    # Should use enums or constants

    if damage_type == "physical":
        return damage - 2
    if damage_type == "magic":
        return damage - 1
    if damage_type == "special":
        return damage
    return damage - 1


def apply_equipment_modifier(
    base_damage: int, weapon_power_bonus: int, rarity_multiplier: float
) -> int:
    """Apply equipment bonuses to damage."""
    total_bonus = int(float(weapon_power_bonus) * rarity_multiplier)
    return base_damage + total_bonus


def modify_damage_by_equipment_quality(damage: int, rarity: str) -> int:
    """Modify damage based on equipment rarity."""
    # String-based rarity is fragile - should use constants
    if rarity == "legendary":
        return int(float(damage) * 1.5)
    if rarity == "epic":
        return int(float(damage) * 1.3)
    if rarity == "rare":
        return int(float(damage) * 1.15)
    return damage


def get_damage_type(weapon_class: str) -> str:
    """Determine damage type from weapon class."""
    # Another string-based fragility
    if weapon_class == "staff":
        return "magic"
    if weapon_class == "dagger":
        return "physical"
    if weapon_class == "sword":
        return "physical"
    if weapon_class == "bow":
        return "physical"
    return "physical"
