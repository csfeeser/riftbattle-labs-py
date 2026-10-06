from models import Fighter
from util import clamp


def apply_healing(target: Fighter, amount: int) -> int:
    if amount <= 0:
        return 0

    before = target.hp
    target.hp = clamp(target.hp + amount, 0, target.max_hp)
    return target.hp - before


def use_healing_potion(target: Fighter) -> str:
    healed = apply_healing(target, 12)
    if healed == 0:
        return f"{target.name} receives no healing."
    return f"{target.name} drinks a potion and restores HP."
