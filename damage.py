from status_effects import has_status
from models import Fighter
from moves import Move


def calculate_damage(attacker: Fighter, defender: Fighter, move: Move) -> int:
    base = move.power + attacker.stats.power
    base = apply_weapon_style_bonus(attacker, base)
    base = apply_critical_hit(attacker, base)
    base = modify_damage_by_element(base, move.element, defender)
    base = modify_damage_by_armor(base, move.damage_type, defender)
    base -= int(defender.stats.defense / 2)  # truncate toward zero, like Go

    if base < 1:
        return 1

    return base


def apply_weapon_style_bonus(attacker: Fighter, damage: int) -> int:
    if attacker.weapon_type == "greatsword":
        return damage + 4
    if attacker.weapon_type == "staff":
        return damage + int(attacker.stats.spirit / 2)
    if attacker.weapon_type == "dagger":
        return damage + int(attacker.stats.agility / 2)
    return damage


def apply_critical_hit(attacker: Fighter, damage: int) -> int:
    if attacker.stats.crit_chance >= 25:
        return damage + int(damage / 2)
    return damage


def modify_damage_by_element(
    damage: int, element: str, defender: Fighter
) -> int:
    if element == "fire" and has_status(defender, "frozen"):
        return damage + 6
    if element == "ice" and has_status(defender, "burning"):
        return damage + 3
    return damage


def modify_damage_by_armor(
    damage: int, damage_type: str, defender: Fighter
) -> int:
    if defender.armor_type == "heavy":
        if damage_type == "physical":
            return damage - 4
        return damage - 1
    if defender.armor_type == "cloth":
        if damage_type == "magic":
            return damage - 1
        return damage
    return damage - 2
