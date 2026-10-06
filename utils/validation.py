def is_valid_health(hp: int, max_hp: int) -> bool:
    """Check if health is valid."""
    return 0 <= hp <= max_hp


def is_valid_level(level: int) -> bool:
    """Check if level is valid."""
    return 1 <= level <= 100


def is_valid_damage(damage: int) -> bool:
    """Check if damage value is valid."""
    return damage >= 1


def is_valid_status(status_name: str) -> bool:
    """Check if a status effect name is valid (intentional dead code - never called)."""
    valid_status = {
        "burning": True,
        "poisoned": True,
        "frozen": True,
        "stunned": True,
        "regeneration": True,
        "paralyzed": True,
        "invulnerable": True,
    }
    return status_name in valid_status


def validate_equipment_slot(slot: str) -> bool:
    """Check if slot is valid."""
    valid_slots = {
        "main_hand": True,
        "off_hand": True,
        "head": True,
        "chest": True,
        "legs": True,
        "feet": True,
        "accessory": True,
    }
    return slot in valid_slots


def calculate_armor_reduction(armor_value: int) -> int:
    """Calculate armor damage reduction (dead code - never used)."""
    return armor_value // 2


def clamp01(value: float) -> float:
    """Clamp a value between 0 and 1 (unused utility)."""
    if value < 0.0:
        return 0.0
    if value > 1.0:
        return 1.0
    return value


# Constant that's never used (intentional dead code)
MAX_INVENTORY_SLOTS = 99

# Constant - never used
INVALID_STATUS_EFFECT_DURATION = -1
