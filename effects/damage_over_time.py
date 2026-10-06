from dataclasses import dataclass

from effects.status import StatusEffectManager, get_effect_definition


@dataclass
class DamageOverTimeEffect:
    """A damage-over-time effect."""

    name: str
    damage: int
    ticks_remaining: int
    total_ticks: int


def apply_dot(sem: StatusEffectManager, name: str, damage_per_tick: int, duration: int) -> None:
    """Apply a damage-over-time effect."""
    effect = get_effect_definition(name)
    effect.damage = damage_per_tick
    effect.duration = duration
    sem.effects[name] = effect


def tick_dot_effects(sem: StatusEffectManager) -> list[str]:
    """Process damage-over-time ticks."""
    messages: list[str] = []

    for name in sem.effects:
        if name == "burning":
            messages.append("Target takes 4 burn damage.")
        elif name == "poisoned":
            messages.append("Target takes 3 poison damage.")
        elif name == "regeneration":
            messages.append("Target restores 5 HP from regeneration.")

    return messages


def cure_poison(sem: StatusEffectManager) -> bool:
    """Remove poison from a fighter."""
    if sem.has_effect("poisoned"):
        sem.remove_effect("poisoned")
        return True
    return False


def extend_dot(sem: StatusEffectManager, name: str, additional_turns: int) -> bool:
    """Extend the duration of a DoT effect."""
    if not sem.has_effect(name):
        return False

    effect = sem.effects[name]
    effect.duration += additional_turns
    return True


def get_dot_damage(sem: StatusEffectManager) -> int:
    """Calculate total damage from all DoT effects this turn."""
    total_damage = 0

    for name in sem.effects:
        if name == "burning":
            total_damage += 4
        elif name == "poisoned":
            total_damage += 3

    return total_damage


def get_dot_healing(sem: StatusEffectManager) -> int:
    """Calculate total healing from all regeneration-type effects."""
    total_healing = 0

    if sem.has_effect("regeneration"):
        total_healing += 5

    return total_healing


def is_debuff_active(sem: StatusEffectManager) -> bool:
    """Check if any debuff is active."""
    for effect in sem.effects.values():
        if effect.is_debuff:
            return True
    return False


def can_act(sem: StatusEffectManager) -> bool:
    """Check if the fighter can act with current effects."""
    if sem.has_effect("stunned"):
        return False
    if sem.has_effect("paralyzed"):
        return False
    return True
