from status_effects import apply_status_effect, tick_status_effects
from healing import use_healing_potion
from models import Stats, new_fighter
from moves import FIREBALL
from turn import resolve_turn


def main() -> None:
    hero = new_fighter(
        "Aria",
        "Mage",
        36,
        "staff",
        "fire",
        "cloth",
        Stats(power=7, defense=3, agility=5, spirit=8, crit_chance=10),
    )
    goblin = new_fighter(
        "Goblin Raider",
        "Monster",
        30,
        "dagger",
        "none",
        "heavy",
        Stats(power=5, defense=4, agility=4, spirit=1, crit_chance=0),
    )

    apply_status_effect(goblin, "frozen", 1)

    result = resolve_turn(hero, goblin, FIREBALL)
    for message in result.messages:
        print(message)

    for message in tick_status_effects(goblin):
        print(message)

    print(f"{goblin.name} HP: {goblin.hp}/{goblin.max_hp}")
    print(use_healing_potion(hero))
    print(f"{hero.name} HP: {hero.hp}/{hero.max_hp}")


if __name__ == "__main__":
    main()
