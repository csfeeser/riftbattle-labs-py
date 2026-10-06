from dataclasses import dataclass


@dataclass
class GameRules:
    """Rules for a game mode."""

    mode_name: str
    allow_items: bool
    allow_fleeing: bool
    damage_multiplier: float
    xp_multiplier: float
    max_turns: int
    allow_respawn: bool
    required_level: int
    reward_gold_multiplier: float


def get_mode_rules(mode_name: str) -> GameRules:
    """Return the rules for a specific game mode."""
    # String-based config is intentional fragility
    if mode_name == "training":
        return GameRules(
            mode_name="Training",
            allow_items=True,
            allow_fleeing=True,
            damage_multiplier=0.8,
            xp_multiplier=1.5,
            max_turns=1000,
            allow_respawn=True,
            required_level=1,
            reward_gold_multiplier=0.5,
        )
    if mode_name == "ranked":
        return GameRules(
            mode_name="Ranked",
            allow_items=False,
            allow_fleeing=False,
            damage_multiplier=1.0,
            xp_multiplier=1.0,
            max_turns=100,
            allow_respawn=False,
            required_level=10,
            reward_gold_multiplier=2.0,
        )
    if mode_name == "story":
        return GameRules(
            mode_name="Story",
            allow_items=True,
            allow_fleeing=True,
            damage_multiplier=1.0,
            xp_multiplier=1.0,
            max_turns=500,
            allow_respawn=False,
            required_level=1,
            reward_gold_multiplier=1.5,
        )
    if mode_name == "arena":
        return GameRules(
            mode_name="Arena",
            allow_items=False,
            allow_fleeing=False,
            damage_multiplier=1.2,
            xp_multiplier=2.0,
            max_turns=50,
            allow_respawn=False,
            required_level=15,
            reward_gold_multiplier=5.0,
        )
    return GameRules(
        mode_name="Unknown",
        allow_items=True,
        allow_fleeing=True,
        damage_multiplier=1.0,
        xp_multiplier=1.0,
        max_turns=100,
        allow_respawn=True,
        required_level=1,
        reward_gold_multiplier=1.0,
    )


def training_mode() -> GameRules:
    """Return training mode rules."""
    return get_mode_rules("training")


def ranked_mode() -> GameRules:
    """Return ranked mode rules."""
    return get_mode_rules("ranked")


def story_mode() -> GameRules:
    """Return story mode rules."""
    return get_mode_rules("story")


def arena_mode() -> GameRules:
    """Return arena mode rules."""
    return get_mode_rules("arena")


def can_enter_mode(fighter_level: int, mode_name: str) -> bool:
    """Check if a fighter can enter a specific mode."""
    rules = get_mode_rules(mode_name)
    return fighter_level >= rules.required_level


def apply_mode_multipliers(base_damage: int, base_xp: int, mode_name: str) -> tuple[int, int]:
    """Apply damage and XP multipliers."""
    rules = get_mode_rules(mode_name)
    adjusted_damage = int(float(base_damage) * rules.damage_multiplier)
    adjusted_xp = int(float(base_xp) * rules.xp_multiplier)
    return adjusted_damage, adjusted_xp
