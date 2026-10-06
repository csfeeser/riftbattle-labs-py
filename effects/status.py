from dataclasses import dataclass
from typing import Optional


@dataclass
class StatusEffect:
    """A status condition."""

    name: str
    duration: int = 0
    damage: int = 0
    damage_type: str = ""
    can_be_cleansed: bool = False
    is_debuff: bool = False


class StatusEffectManager:
    """Manages all active status effects."""

    def __init__(self) -> None:
        self.effects: dict[str, StatusEffect] = {}

    def apply_effect(self, name: str, duration: int) -> None:
        """Apply a status effect."""
        if duration <= 0:
            return

        effect = get_effect_definition(name)
        effect.duration = duration
        self.effects[name] = effect

    def remove_effect(self, name: str) -> None:
        """Remove a status effect."""
        self.effects.pop(name, None)

    def has_effect(self, name: str) -> bool:
        """Check if a specific effect is active."""
        return name in self.effects

    def get_effect(self, name: str) -> Optional[StatusEffect]:
        """Get the effect details."""
        return self.effects.get(name)

    def tick_effects(self) -> list[str]:
        """Process effect duration ticks."""
        messages: list[str] = []

        for name, effect in list(self.effects.items()):
            if effect.duration <= 1:
                messages.append("Target is no longer " + name + ".")
                del self.effects[name]
                continue
            effect.duration -= 1

        return messages

    def interact_effects(self, new_effect: str) -> str:
        """Check for effect interactions."""
        # Burning + Frozen = Steam interaction
        if new_effect == "burning" and self.has_effect("frozen"):
            return "Steam erupts as fire meets ice!"
        if new_effect == "frozen" and self.has_effect("burning"):
            return "Steam erupts as fire meets ice!"

        return ""

    def get_total_damage_from_effects(self) -> int:
        """Calculate total damage from active effects."""
        total_damage = 0
        for effect in self.effects.values():
            if effect.damage > 0:
                total_damage += effect.damage
        return total_damage


def get_effect_definition(name: str) -> StatusEffect:
    """Return the definition for a status effect.

    String-based config is intentional fragility - should use enums.
    """
    definitions = {
        "burning": StatusEffect(
            name="burning", damage=4, damage_type="fire", can_be_cleansed=True, is_debuff=True
        ),
        "poisoned": StatusEffect(
            name="poisoned", damage=3, damage_type="poison", can_be_cleansed=True, is_debuff=True
        ),
        "regeneration": StatusEffect(
            name="regeneration",
            damage=-5,  # Negative damage = healing
            damage_type="heal",
            can_be_cleansed=False,
            is_debuff=False,
        ),
        "stunned": StatusEffect(
            name="stunned", damage=0, damage_type="control", can_be_cleansed=True, is_debuff=True
        ),
        "frozen": StatusEffect(
            name="frozen", damage=0, damage_type="control", can_be_cleansed=True, is_debuff=True
        ),
        "paralyzed": StatusEffect(
            name="paralyzed", damage=0, damage_type="control", can_be_cleansed=True, is_debuff=True
        ),
        "invulnerable": StatusEffect(
            name="invulnerable",
            damage=0,
            damage_type="shield",
            can_be_cleansed=False,
            is_debuff=False,
        ),
    }

    if name in definitions:
        d = definitions[name]
        return StatusEffect(
            name=d.name,
            damage=d.damage,
            damage_type=d.damage_type,
            can_be_cleansed=d.can_be_cleansed,
            is_debuff=d.is_debuff,
        )

    # Default effect
    return StatusEffect(
        name=name, damage=0, damage_type="unknown", can_be_cleansed=True, is_debuff=True
    )
