from damage import calculate_damage
from status_effects import apply_status_effect, has_status
from models import Fighter
from moves import Move, TurnResult
from rules import is_defeated
from util import clamp


def resolve_turn(attacker: Fighter, defender: Fighter, move: Move) -> TurnResult:
    result = TurnResult(
        actor=attacker.name,
        target=defender.name,
        move=move.name,
    )

    if has_status(attacker, "stunned"):
        result.messages.append(f"{attacker.name} is stunned and loses the turn.")
        return result

    damage = calculate_damage(attacker, defender, move)
    defender.hp = clamp(defender.hp - damage, 0, defender.max_hp)
    result.damage = damage
    result.messages.append(
        f"{attacker.name} uses {move.name} for {damage} damage."
    )

    if move.applies_effect:
        apply_status_effect(defender, move.applies_effect, move.effect_duration)
        result.messages.append(
            f"{defender.name} is now {move.applies_effect}."
        )

    if is_defeated(defender):
        result.messages.append(f"{defender.name} is defeated.")

    return result
