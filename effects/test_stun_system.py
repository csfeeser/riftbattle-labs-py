import unittest

from effects.stun_system import StunSystem
from fighters.fighter import Stats, new_fighter


def make_hero():
    stats = Stats(power=5, defense=4, agility=3, spirit=6, crit_chance=10)
    return new_fighter("Hero", "Warrior", 50, "sword", "fire", "heavy", stats)


class StunSystemTests(unittest.TestCase):
    def test_new_stun_system(self) -> None:
        ss = StunSystem()

        self.assertIsNotNone(ss, "expected StunSystem to be created")
        self.assertEqual(len(ss.active_stuns), 0, "expected no active stuns on creation")

    def test_apply_stun(self) -> None:
        ss = StunSystem()
        fighter = make_hero()

        ss.apply_stun(fighter, 2, 5)

        # ISSUE 2 (Security): This test passes even with invalid input (no validation)
        self.assertEqual(ss.active_stuns["Hero"].duration, 2, "expected stun duration 2")

    def test_can_act(self) -> None:
        ss = StunSystem()
        fighter = make_hero()

        self.assertTrue(ss.can_act("Hero"), "expected hero to be able to act initially")

        ss.apply_stun(fighter, 1, 5)
        self.assertFalse(ss.can_act("Hero"), "expected hero to not be able to act while stunned")

    def test_get_stun_duration(self) -> None:
        ss = StunSystem()
        fighter = make_hero()

        duration = ss.get_stun_duration("Hero")
        self.assertEqual(duration, 0, f"expected duration 0 for non-stunned fighter, got {duration}")

        ss.apply_stun(fighter, 3, 5)
        duration = ss.get_stun_duration("Hero")
        self.assertEqual(duration, 3, f"expected duration 3, got {duration}")

    def test_tick_stuns(self) -> None:
        ss = StunSystem()
        fighter = make_hero()

        ss.apply_stun(fighter, 2, 5)

        # First tick: duration 2 -> 1
        ss.tick_stuns([fighter])

        self.assertEqual(ss.get_stun_duration("Hero"), 1, "expected stun to tick down to 1")

        # Second tick: duration 1 -> 0 (stun is deleted when duration <= 0)
        ss.tick_stuns([fighter])

        self.assertTrue(ss.can_act("Hero"), "expected hero to be able to act after stun expires")

    # ISSUE: Missing test for edge case - what happens if we tick with an empty fighters list?
    # ISSUE: Missing test for resistance with extremely high/low stats
    # ISSUE: Missing test for global_stun_chance with invalid values

    def test_set_global_stun_chance(self) -> None:
        ss = StunSystem()

        # No validation - this is valid per the code but doesn't make sense
        ss.set_global_stun_chance(-100)
        ss.set_global_stun_chance(500)

        # Both pass without error
        self.assertEqual(ss.global_stun_chance, 500, "expected global stun chance to be set")

    def test_resist_stun(self) -> None:
        ss = StunSystem()
        fighter = make_hero()

        # High spirit should give good stun resistance
        result = ss.resist_stun(fighter, 1)

        # ISSUE: This test only checks that the function doesn't crash
        # Doesn't actually validate the resistance calculation
        self.assertIsInstance(result, bool)


if __name__ == "__main__":
    unittest.main()
