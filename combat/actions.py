from dataclasses import dataclass, field
from typing import Any

from combat.moves import get_move

# Action types
ACTION_ATTACK = "attack"
ACTION_DEFEND = "defend"
ACTION_CAST = "cast"
ACTION_ITEM = "item"
ACTION_FLEE = "flee"
ACTION_STANCE = "stance"


@dataclass
class Action:
    """An action a fighter takes in combat."""

    action_type: str
    source_name: str
    target_name: str = ""
    move_name: str = ""
    item_id: str = ""
    parameters: dict[str, Any] = field(default_factory=dict)
    timestamp: int = 0


def new_attack_action(source_name: str, target_name: str, move_name: str) -> Action:
    """Create an attack action."""
    return Action(ACTION_ATTACK, source_name, target_name=target_name, move_name=move_name)


def new_defend_action(source_name: str) -> Action:
    """Create a defend action."""
    return Action(ACTION_DEFEND, source_name)


def new_cast_action(source_name: str, target_name: str, spell_name: str) -> Action:
    """Create a spell casting action."""
    return Action(ACTION_CAST, source_name, target_name=target_name, move_name=spell_name)


def new_item_action(source_name: str, target_name: str, item_id: str) -> Action:
    """Create an item use action."""
    return Action(ACTION_ITEM, source_name, target_name=target_name, item_id=item_id)


def new_flee_action(source_name: str) -> Action:
    """Create a flee action."""
    return Action(ACTION_FLEE, source_name)


def is_control_action(action: Action) -> bool:
    """Check if action is control-type (stun, paralyze)."""
    move = get_move(action.move_name)
    if move is None:
        return False
    return move.applies_effect == "stunned" or move.applies_effect == "paralyzed"


def validate_action(action: Action) -> bool:
    """Check if an action is valid."""
    # Missing validation - intentional fragility
    # Should validate:
    # 1. Source can act (not stunned, not dead)
    # 2. Move exists
    # 3. MP is sufficient
    # 4. Target exists
    # 5. Target is valid (not already dead, etc)

    return True
