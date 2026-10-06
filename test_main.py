import unittest

from damage import calculate_damage
from status_effects import apply_status_effect
from healing import use_healing_potion
from models import Stats, new_fighter
from moves import FIREBALL
from rules import can_act


class RiftBattleTests(unittest.TestCase):
    def test_fire_damage_against_frozen_enemy_gets_bonus(self) -> None:
        mage = new_fighter(
            "Mage",
            "Caster",
            30,
            "staff",
            "fire",
            "cloth",
            Stats(power=6, defense=2, agility=4, spirit=7, crit_chance=0),
        )
        target = new_fighter(
            "Target",
            "Dummy",
            40,
            "none",
            "none",
            "light",
            Stats(power=1, defense=4, agility=1, spirit=1, crit_chance=0),
        )
        apply_status_effect(target, "frozen", 1)

        damage = calculate_damage(mage, target, FIREBALL)
        self.assertGreaterEqual(damage, 18)

    def test_healing_potion_restores_health(self) -> None:
        hero = new_fighter(
            "Hero",
            "Warrior",
            40,
            "greatsword",
            "none",
            "heavy",
            Stats(power=7, defense=6, agility=3, spirit=2, crit_chance=0),
        )
        hero.hp = 20

        use_healing_potion(hero)
        self.assertGreater(hero.hp, 20)

    def test_stunned_target_cannot_act(self) -> None:
        knight = new_fighter(
            "Knight",
            "Tank",
            45,
            "greatsword",
            "none",
            "heavy",
            Stats(power=8, defense=8, agility=2, spirit=1, crit_chance=0),
        )
        apply_status_effect(knight, "stunned", 1)

        self.assertFalse(can_act(knight))


if __name__ == "__main__":
    unittest.main()
