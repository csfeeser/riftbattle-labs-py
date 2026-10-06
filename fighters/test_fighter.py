import unittest

from fighters.fighter import Stats, new_fighter
from fighters.progression import ProgressionTracker


def make_hero():
    stats = Stats(power=5, defense=4, agility=3, spirit=6, crit_chance=10)
    return new_fighter("Hero", "Warrior", 50, "sword", "fire", "heavy", stats)


def make_mage():
    stats = Stats(power=5, defense=4, agility=3, spirit=6, crit_chance=10)
    return new_fighter("Mage", "Caster", 30, "staff", "fire", "cloth", stats)


class FighterTests(unittest.TestCase):
    def test_new_fighter_initialization(self) -> None:
        fighter = make_hero()

        self.assertEqual(fighter.name, "Hero")
        self.assertEqual((fighter.hp, fighter.max_hp), (50, 50), f"expected HP 50, got {fighter.hp}")
        self.assertEqual(fighter.level, 1, f"expected level 1, got {fighter.level}")
        self.assertTrue(fighter.has_skill("attack"), "expected fighter to start with attack skill")

    def test_add_xp_and_level_up(self) -> None:
        fighter = make_hero()

        initial_power = fighter.stats.power

        # Add XP to trigger level up (need 100 XP at level 1)
        fighter.add_xp(100)

        self.assertEqual(fighter.level, 2, f"expected level 2 after 100 XP, got {fighter.level}")
        self.assertGreater(fighter.stats.power, initial_power, "expected stats to improve on level up")
        self.assertEqual(fighter.xp, 0, f"expected XP to reset on level up, got {fighter.xp}")

    def test_skill_unlock(self) -> None:
        fighter = make_mage()

        # At level 1, should only have attack
        self.assertFalse(fighter.has_skill("power_strike"), "power_strike should not be unlocked at level 1")

        # Level up 4 times to reach level 5
        for _ in range(4):
            fighter.add_xp(100)

        self.assertTrue(fighter.has_skill("power_strike"), "power_strike should be unlocked at level 5")

    def test_can_perform_action(self) -> None:
        fighter = make_hero()

        # Should be able to perform basic attack
        self.assertTrue(fighter.can_perform_action("attack"), "expected fighter to be able to attack")

        # Should not be able to perform a skill that is not unlocked yet
        self.assertFalse(
            fighter.can_perform_action("power_strike"), "expected fighter to not have power_strike at level 1"
        )

        # Apply stun
        fighter.status["stunned"] = 1
        self.assertFalse(fighter.can_perform_action("attack"), "expected stunned fighter to not be able to act")

    def test_adjust_health(self) -> None:
        fighter = make_hero()

        fighter.hp = 30
        healed = fighter.adjust_health(10)

        self.assertEqual(fighter.hp, 40, f"expected HP 40, got {fighter.hp}")
        self.assertEqual(healed, 10, f"expected healing to return 10, got {healed}")

        # Overheal should clamp to max_hp
        fighter.adjust_health(100)
        self.assertEqual(fighter.hp, 50, f"expected HP to clamp to max_hp 50, got {fighter.hp}")

    def test_restore_mana(self) -> None:
        fighter = make_mage()

        fighter.mp = 5
        restored = fighter.restore_mana(5)

        self.assertEqual(fighter.mp, 10, f"expected MP 10, got {fighter.mp}")
        self.assertEqual(restored, 5, f"expected mana restore to return 5, got {restored}")

    def test_progression_tracker(self) -> None:
        fighter = make_hero()
        tracker = ProgressionTracker(fighter)

        # Test XP multiplier
        tracker.set_xp_multiplier(2.0)
        tracker.gain_xp(40)  # Should gain 80 XP with 2x multiplier

        self.assertEqual(fighter.xp, 80, f"expected 80 XP with 2x multiplier, got {fighter.xp}")

        # Complete level up
        tracker.gain_xp(20)  # Gains 40 XP, total 120, triggers level up
        self.assertEqual(fighter.level, 2, f"expected level 2, got {fighter.level}")

    def test_is_defeated(self) -> None:
        fighter = make_hero()

        self.assertFalse(fighter.is_defeated(), "expected fighter to not be defeated at full health")

        fighter.hp = 0
        self.assertTrue(fighter.is_defeated(), "expected fighter to be defeated at 0 HP")


if __name__ == "__main__":
    unittest.main()
