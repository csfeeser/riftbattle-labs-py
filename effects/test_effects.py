import unittest

from effects.damage_over_time import (
    can_act,
    cure_poison,
    extend_dot,
    get_dot_damage,
    get_dot_healing,
    is_debuff_active,
)
from effects.status import StatusEffectManager, get_effect_definition


class EffectsTests(unittest.TestCase):
    def test_status_effect_manager(self) -> None:
        sem = StatusEffectManager()

        sem.apply_effect("burning", 2)

        self.assertTrue(sem.has_effect("burning"), "expected burning effect to be active")
        self.assertFalse(sem.has_effect("poisoned"), "expected poisoned effect to not be active")

    def test_effect_definition(self) -> None:
        burning = get_effect_definition("burning")

        self.assertEqual(burning.name, "burning")
        self.assertEqual(burning.damage, 4, f"expected 4 burn damage, got {burning.damage}")
        self.assertTrue(burning.is_debuff, "expected burning to be a debuff")

    def test_tick_effects(self) -> None:
        sem = StatusEffectManager()
        sem.apply_effect("burning", 2)
        sem.apply_effect("poisoned", 1)

        messages = sem.tick_effects()

        # poisoned should expire (was 1 turn)
        self.assertFalse(sem.has_effect("poisoned"), "expected poisoned to expire after tick")

        # burning should still be active (was 2 turns, now 1)
        self.assertTrue(sem.has_effect("burning"), "expected burning to still be active")

        # Should have message about poisoned expiring
        self.assertNotEqual(len(messages), 0, "expected tick messages")

    def test_remove_effect(self) -> None:
        sem = StatusEffectManager()
        sem.apply_effect("frozen", 3)

        self.assertTrue(sem.has_effect("frozen"), "expected frozen to be active")

        sem.remove_effect("frozen")

        self.assertFalse(sem.has_effect("frozen"), "expected frozen to be removed")

    def test_effect_interactions(self) -> None:
        sem = StatusEffectManager()
        sem.apply_effect("frozen", 1)

        message = sem.interact_effects("burning")

        self.assertNotEqual(message, "", "expected interaction message for burning + frozen")

    def test_get_total_damage_from_effects(self) -> None:
        sem = StatusEffectManager()
        sem.apply_effect("burning", 1)
        sem.apply_effect("poisoned", 1)

        total_damage = sem.get_total_damage_from_effects()
        expected_damage = 4 + 3

        self.assertEqual(total_damage, expected_damage)

    def test_dot_damage(self) -> None:
        sem = StatusEffectManager()
        sem.apply_effect("burning", 2)
        sem.apply_effect("poisoned", 1)

        damage = get_dot_damage(sem)
        expected_damage = 4 + 3

        self.assertEqual(damage, expected_damage)

    def test_dot_healing(self) -> None:
        sem = StatusEffectManager()
        sem.apply_effect("regeneration", 2)

        healing = get_dot_healing(sem)

        self.assertEqual(healing, 5, f"expected 5 healing from regen, got {healing}")

    def test_can_act_with_effects(self) -> None:
        sem = StatusEffectManager()

        self.assertTrue(can_act(sem), "expected to be able to act with no effects")

        sem.apply_effect("stunned", 1)

        self.assertFalse(can_act(sem), "expected to not be able to act while stunned")

        sem.remove_effect("stunned")
        sem.apply_effect("burning", 1)

        self.assertTrue(can_act(sem), "expected to be able to act while burning")

    def test_cure_poison(self) -> None:
        sem = StatusEffectManager()
        sem.apply_effect("poisoned", 3)

        self.assertTrue(sem.has_effect("poisoned"), "expected poisoned to be active")

        cured = cure_poison(sem)

        self.assertTrue(cured, "expected poison to be cured")
        self.assertFalse(sem.has_effect("poisoned"), "expected poisoned to be removed")

    def test_extend_dot(self) -> None:
        sem = StatusEffectManager()
        sem.apply_effect("burning", 2)

        extended = extend_dot(sem, "burning", 3)

        self.assertTrue(extended, "expected DoT to be extended")

        effect = sem.get_effect("burning")
        self.assertEqual(effect.duration, 5, f"expected duration 5, got {effect.duration}")

    def test_is_debuff_active(self) -> None:
        sem = StatusEffectManager()

        self.assertFalse(is_debuff_active(sem), "expected no debuffs active initially")

        sem.apply_effect("burning", 1)

        self.assertTrue(is_debuff_active(sem), "expected debuff to be active")

        sem.remove_effect("burning")
        sem.apply_effect("regeneration", 1)

        self.assertFalse(is_debuff_active(sem), "expected regeneration to not be a debuff")


if __name__ == "__main__":
    unittest.main()
