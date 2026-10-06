from typing import Optional

from equipment.equipment import (
    TYPE_ACCESSORY,
    TYPE_ARMOR,
    TYPE_WEAPON,
    Equipment,
)

# FighterEquipmentIntegration provides functions to integrate equipment with fighters
# Note: This creates some tight coupling that could be refactored


def equip_item(
    equipment: Optional[Equipment], current_equipped: dict[str, Equipment], slot: str
) -> Optional[Equipment]:
    """Safely equip an item to a fighter.

    Handles slot conflicts by returning the unequipped item.
    """
    # Return the previously equipped item (if any)
    previous_item = current_equipped.get(slot)

    if equipment is None:
        if previous_item is not None:
            del current_equipped[slot]
        return previous_item

    # Store the new equipment
    current_equipped[slot] = equipment
    return previous_item


def unequip_item(current_equipped: dict[str, Equipment], slot: str) -> Optional[Equipment]:
    """Remove equipment from a slot."""
    if slot in current_equipped:
        return current_equipped.pop(slot)
    return None


def calculate_fighter_stat_bonus(equipped: dict[str, Equipment]) -> tuple[int, int, int, int]:
    """Calculate total stat bonuses from all equipped items."""
    total_power = 0
    total_defense = 0
    total_agility = 0
    total_spirit = 0

    for item in equipped.values():
        if item is None:
            continue

        # Apply rarity multiplier
        multiplier = item.get_rarity_bonus()
        total_power += int(float(item.power_bonus) * multiplier)
        total_defense += int(float(item.defense_bonus) * multiplier)
        total_agility += int(float(item.agility_bonus) * multiplier)
        total_spirit += int(float(item.spirit_bonus) * multiplier)

    return total_power, total_defense, total_agility, total_spirit


# Defines which item types can go in which slots
EQUIPMENT_SLOT_RESTRICTIONS: dict[str, list[str]] = {
    "main_hand": [TYPE_WEAPON],
    "off_hand": [TYPE_WEAPON, TYPE_ACCESSORY],
    "head": [TYPE_ARMOR, TYPE_ACCESSORY],
    "chest": [TYPE_ARMOR],
    "legs": [TYPE_ARMOR],
    "feet": [TYPE_ARMOR, TYPE_ACCESSORY],
    "accessory": [TYPE_ACCESSORY],
}


def is_valid_slot_for_type(slot: str, equip_type: str) -> bool:
    """Check if an equipment type can go in a slot."""
    if slot in EQUIPMENT_SLOT_RESTRICTIONS:
        for t in EQUIPMENT_SLOT_RESTRICTIONS[slot]:
            if t == equip_type:
                return True
    return False


def get_equipped_items(equipped: dict[str, Equipment]) -> list[Equipment]:
    """Return a list of all currently equipped items."""
    items: list[Equipment] = []
    for item in equipped.values():
        if item is not None:
            items.append(item)
    return items


def can_equip_multiple(equipment: Equipment, currently_equipped: list[Equipment]) -> bool:
    """Check if a fighter can equip duplicate items.

    Some equipment might have restrictions on duplicates.
    """
    # For now, allow all duplicates
    # This could be extended to check for unique items
    return True
