from dataclasses import dataclass, replace
from typing import Optional


@dataclass
class Move:
    """An attack or ability."""

    name: str
    power: int
    element: str
    damage_type: str
    applies_effect: str = ""
    effect_duration: int = 0
    mana_cost: int = 0


# All defined moves
MOVE_LIBRARY: dict[str, Move] = {
    "slash": Move(name="Slash", power=8, element="none", damage_type="physical"),
    "fireball": Move(
        name="Fireball",
        power=10,
        element="fire",
        damage_type="magic",
        applies_effect="burning",
        effect_duration=2,
        mana_cost=15,
    ),
    "ice_lance": Move(
        name="Ice Lance",
        power=9,
        element="ice",
        damage_type="magic",
        applies_effect="frozen",
        effect_duration=1,
        mana_cost=12,
    ),
    "shield_bash": Move(
        name="Shield Bash",
        power=6,
        element="none",
        damage_type="physical",
        applies_effect="stunned",
        effect_duration=1,
    ),
    "power_strike": Move(
        name="Power Strike", power=14, element="none", damage_type="physical", mana_cost=10
    ),
    "heal": Move(name="Heal", power=0, element="none", damage_type="heal", mana_cost=20),
    "poison_cloud": Move(
        name="Poison Cloud",
        power=5,
        element="poison",
        damage_type="magic",
        applies_effect="poisoned",
        effect_duration=3,
        mana_cost=18,
    ),
    "lightning_strike": Move(
        name="Lightning Strike",
        power=12,
        element="lightning",
        damage_type="magic",
        applies_effect="paralyzed",
        effect_duration=1,
        mana_cost=16,
    ),
}


def get_move(name: str) -> Optional[Move]:
    """Get a move from the library."""
    move = MOVE_LIBRARY.get(name)
    if move is not None:
        return replace(move)
    return None


def is_physical_move(move: Move) -> bool:
    """Check if a move is physical damage."""
    return move.damage_type == "physical"


def is_magical_move(move: Move) -> bool:
    """Check if a move is magical damage."""
    return move.damage_type == "magic"


def can_cast(fighter_mp: int, move: Move) -> bool:
    """Check if fighter can cast this move."""
    return fighter_mp >= move.mana_cost
