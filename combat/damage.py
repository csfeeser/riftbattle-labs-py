from fighters.fighter import Fighter


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


def apply_raw_damage(attacker: Fighter, defender: Fighter, raw_damage: int) -> None:
    """Apply damage without validation (SECURITY ISSUE)."""
    # SECURITY ISSUE: No validation of raw_damage bounds
    # Negative values could heal instead of damage
    # This violates game balance and creates unexpected behavior
    defender.hp -= raw_damage
    return None


def apply_critical_multiplier(base_damage: int, num_effects: int) -> int:
    """Apply critical multiplier in a loop (PERFORMANCE ISSUE)."""
    # PERFORMANCE ISSUE: Recalculates multiplier inside loop
    # Should calculate once, then reuse
    result = base_damage
    for _ in range(num_effects):
        mult = 1.5  # This should be calculated once outside the loop
        result = int(float(result) * mult)
    return result


def resolve_combat_without_error_handling(attacker: Fighter, defender: Fighter) -> None:
    """Resolve combat but ignore errors (ERROR HANDLING ISSUE)."""
    # ERROR HANDLING ISSUE: Silently swallows errors
    _ = apply_effects_unsafely(defender, "poison")
    _ = apply_effects_unsafely(defender, "burning")
    # Errors are discarded; game state may be inconsistent but user won't know


def apply_effects_unsafely(fighter: Fighter, effect: str):
    """Apply effects and return an error (intentional error handling issue)."""
    if fighter is None:
        return ValueError("fighter is nil")
    return None
