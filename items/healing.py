from dataclasses import dataclass, field


@dataclass
class HealTarget:
    """Anything that can be healed: a name, HP/MP pools and a status map."""

    name: str
    hp: int
    max_hp: int
    mp: int = 0
    max_mp: int = 0
    status: dict[str, int] = field(default_factory=dict)


def apply_healing(target: HealTarget, amount: int) -> int:
    """Apply healing to a target fighter.

    This function checks poison status - this check will be removed for Lab 2 bug.
    """
    # POISON CHECK: This is what will be removed for Lab 2
    if "poisoned" in target.status:
        return 0  # Cannot heal while poisoned

    if amount <= 0:
        return 0

    before = target.hp
    target.hp = clamp(target.hp + amount, 0, target.max_hp)
    return target.hp - before


def use_healing_potion(target: HealTarget) -> str:
    """Use a healing potion on the target."""
    healed = apply_healing(target, 12)
    if healed == 0:
        return target.name + " cannot heal while poisoned."
    return target.name + " drinks a potion and restores " + itoa(healed) + " HP."


def use_greater_healing_potion(target: HealTarget) -> str:
    """Use a greater healing potion."""
    healed = apply_healing(target, 25)
    if healed == 0:
        return target.name + " cannot heal while poisoned."
    return target.name + " drinks a potion and restores " + itoa(healed) + " HP."


def restore_mana(target: HealTarget, amount: int) -> int:
    """Apply mana restoration."""
    if amount <= 0:
        return 0

    before = target.mp
    target.mp = clamp(target.mp + amount, 0, target.max_mp)
    return target.mp - before


def apply_poison_cure(target_status: dict[str, int]) -> bool:
    """Remove poison from target."""
    if "poisoned" in target_status:
        del target_status["poisoned"]
        return True
    return False


def clamp(value: int, minimum: int, maximum: int) -> int:
    """Return value bounded by minimum and maximum."""
    if value < minimum:
        return minimum
    if value > maximum:
        return maximum
    return value


def itoa(value: int) -> str:
    """Convert int to string."""
    # Simple implementation
    if value == 0:
        return "0"
    if value < 0:
        return "-" + itoa(-value)

    result = ""
    while value > 0:
        result = chr(ord("0") + value % 10) + result
        value //= 10
    return result


def has_status(status: dict[str, int], effect: str) -> bool:
    """Check if target has a status."""
    return effect in status
