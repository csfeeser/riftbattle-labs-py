from dataclasses import dataclass, field

from combat.damage import calculate_damage, calculate_damage_with_critical
from combat.moves import Move


@dataclass
class TurnResult:
    """The result of a turn action."""

    actor: str = ""
    target: str = ""
    move: str = ""
    damage: int = 0
    healed: int = 0
    messages: list[str] = field(default_factory=list)
    hit: bool = False


def resolve_turn(
    attacker_power: int,
    attacker_crit: int,
    defender_defense: int,
    attacker_status: dict[str, int],
    defender_status: dict[str, int],
    move: Move,
) -> TurnResult:
    """Resolve a combat turn for an attacker vs defender."""
    result = TurnResult(hit=True)

    # Check if attacker is stunned
    if "stunned" in attacker_status:
        result.messages.append("Attacker is stunned and loses the turn.")
        result.hit = False
        return result

    # Check if attacker is paralyzed
    if "paralyzed" in attacker_status:
        # 50% chance to act while paralyzed
        # For now, just skip
        result.messages.append("Attacker is paralyzed and cannot act.")
        result.hit = False
        return result

    # Calculate damage
    damage = calculate_damage(
        move.power + attacker_power,
        defender_defense,
        move.element,
        move.damage_type,
        defender_status,
    )
    damage = calculate_damage_with_critical(damage, attacker_crit)
    result.damage = damage
    result.move = move.name

    # Apply status effect
    if move.applies_effect != "":
        defender_status[move.applies_effect] = move.effect_duration
        result.messages.append("Target is now " + move.applies_effect + ".")

    return result


def resolve_damage_over_time(fighter_status: dict[str, int]) -> tuple[int, list[str]]:
    """Apply damage-over-time effects."""
    total_damage = 0
    messages: list[str] = []

    if "burning" in fighter_status:
        total_damage += 4
        messages.append("Fighter takes 4 burn damage.")

    if "poisoned" in fighter_status:
        total_damage += 3
        messages.append("Fighter takes 3 poison damage.")

    if "regeneration" in fighter_status:
        total_damage -= 5
        messages.append("Fighter restores 5 HP from regeneration.")

    return total_damage, messages


def resolve_defense(base_damage: int, defense_level: int) -> int:
    """Calculate defense effectiveness."""
    # Simple defense formula
    reduction = int(defense_level / 2)  # truncate toward zero, like Go
    final_damage = base_damage - reduction
    if final_damage < 1:
        return 1
    return final_damage
