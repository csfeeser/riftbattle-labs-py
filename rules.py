from status_effects import has_status
from models import Fighter


def is_defeated(target: Fighter) -> bool:
    return target.hp <= 0


def can_act(target: Fighter) -> bool:
    return not has_status(target, "stunned") and not is_defeated(target)
