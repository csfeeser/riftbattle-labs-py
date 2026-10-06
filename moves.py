from dataclasses import dataclass, field


@dataclass(frozen=True)
class Move:
    name: str
    power: int
    element: str
    damage_type: str
    applies_effect: str = ""
    effect_duration: int = 0


@dataclass
class TurnResult:
    actor: str
    target: str
    move: str
    damage: int = 0
    messages: list[str] = field(default_factory=list)


SLASH = Move(name="Slash", power=8, element="none", damage_type="physical")
FIREBALL = Move(
    name="Fireball",
    power=10,
    element="fire",
    damage_type="magic",
    applies_effect="burning",
    effect_duration=2,
)
ICE_LANCE = Move(
    name="Ice Lance",
    power=9,
    element="ice",
    damage_type="magic",
    applies_effect="frozen",
    effect_duration=1,
)
SHIELD_BASH = Move(
    name="Shield Bash",
    power=6,
    element="none",
    damage_type="physical",
    applies_effect="stunned",
    effect_duration=1,
)
