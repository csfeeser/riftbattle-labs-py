from typing import Optional

from equipment.equipment import (
    RARITY_COMMON,
    RARITY_EPIC,
    RARITY_LEGENDARY,
    RARITY_RARE,
    RARITY_UNCOMMON,
    Equipment,
)


def format_equipment_name(equipment: Optional[Equipment]) -> str:
    """Return a formatted display name for equipment."""
    if equipment is None:
        return "Empty"

    rarity_prefix = get_rarity_prefix(equipment.rarity)
    return rarity_prefix + equipment.name


def get_rarity_prefix(rarity: str) -> str:
    """Return a color/prefix code for the rarity."""
    if rarity == RARITY_COMMON:
        return "[C] "
    if rarity == RARITY_UNCOMMON:
        return "[U] "
    if rarity == RARITY_RARE:
        return "[R] "
    if rarity == RARITY_EPIC:
        return "[E] "
    if rarity == RARITY_LEGENDARY:
        return "[L] "
    return ""


def describe_equipment(equipment: Optional[Equipment]) -> str:
    """Return a full description of equipment."""
    if equipment is None:
        return "No equipment"

    desc = format_equipment_name(equipment) + "\n"
    desc += "  Type: " + equipment.equipment_type + "\n"

    if equipment.power_bonus > 0:
        desc += "  +Power: " + str(int(float(equipment.power_bonus) * equipment.get_rarity_bonus())) + "\n"
    if equipment.defense_bonus > 0:
        desc += "  +Defense: " + str(int(float(equipment.defense_bonus) * equipment.get_rarity_bonus())) + "\n"
    if equipment.agility_bonus > 0:
        desc += "  +Agility: " + str(equipment.agility_bonus) + "\n"
    if equipment.spirit_bonus > 0:
        desc += "  +Spirit: " + str(equipment.spirit_bonus) + "\n"

    if equipment.required_level > 1:
        desc += "  Required Level: " + str(equipment.required_level) + "\n"

    if len(equipment.effect_resist) > 0:
        desc += "  Resistances:\n"
        for effect, resistance in equipment.effect_resist.items():
            desc += "    " + effect + ": " + str(resistance) + "%\n"

    return desc


def compare_equipment(current: Optional[Equipment], candidate: Optional[Equipment]) -> str:
    """Compare two pieces of equipment."""
    if current is None and candidate is not None:
        return "Candidate is a new item"
    if current is None or candidate is None:
        return "Cannot compare"

    current_power = int(float(current.power_bonus) * current.get_rarity_bonus())
    candidate_power = int(float(candidate.power_bonus) * candidate.get_rarity_bonus())

    if candidate_power > current_power:
        return "Candidate is " + str(candidate_power - current_power) + " power stronger"
    if candidate_power < current_power:
        return "Current is " + str(current_power - candidate_power) + " power stronger"

    return "Equipment has equal power"


def list_equipped_items(equipped: dict[str, Equipment]) -> str:
    """Return a formatted list of equipped items."""
    listing = "Currently Equipped:\n"

    slots = ["main_hand", "off_hand", "head", "chest", "legs", "feet", "accessory"]
    for slot in slots:
        item = equipped.get(slot)
        if item is not None:
            listing += "  " + slot + ": " + format_equipment_name(item) + "\n"
        else:
            listing += "  " + slot + ": [Empty]\n"

    return listing
