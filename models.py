from dataclasses import dataclass, field


@dataclass
class Stats:
    power: int
    defense: int
    agility: int
    spirit: int
    crit_chance: int


@dataclass
class Fighter:
    name: str
    fighter_class: str
    hp: int
    max_hp: int
    weapon_type: str
    element: str
    armor_type: str
    stats: Stats
    status: dict[str, int] = field(default_factory=dict)
    training_mode: bool = False


def new_fighter(
    name: str,
    fighter_class: str,
    hp: int,
    weapon_type: str,
    element: str,
    armor_type: str,
    stats: Stats,
) -> Fighter:
    return Fighter(
        name=name,
        fighter_class=fighter_class,
        hp=hp,
        max_hp=hp,
        weapon_type=weapon_type,
        element=element,
        armor_type=armor_type,
        stats=stats,
    )
