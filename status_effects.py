from models import Fighter
from util import clamp


def apply_status_effect(target: Fighter, effect: str, turns: int) -> None:
    if turns <= 0:
        return
    target.status[effect] = turns


def tick_status_effects(target: Fighter) -> list[str]:
    messages: list[str] = []

    if has_status(target, "burning"):
        target.hp -= 4
        messages.append(f"{target.name} takes 4 burn damage.")

    if has_status(target, "poisoned"):
        target.hp -= 3
        messages.append(f"{target.name} takes 3 poison damage.")

    if has_status(target, "regeneration"):
        target.hp = clamp(target.hp + 5, 0, target.max_hp)
        messages.append(f"{target.name} restores 5 HP from regeneration.")

    for effect, turns in list(target.status.items()):
        if turns <= 1:
            del target.status[effect]
            continue
        target.status[effect] = turns - 1

    return messages


def has_status(target: Fighter, effect: str) -> bool:
    return effect in target.status
