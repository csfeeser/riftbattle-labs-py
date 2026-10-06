import unittest

from combat.actions import (
    ACTION_ATTACK,
    ACTION_CAST,
    ACTION_DEFEND,
    new_attack_action,
    new_cast_action,
    new_defend_action,
)
from combat.damage import calculate_damage, calculate_damage_with_critical
from combat.moves import can_cast, get_move, is_physical_move
from combat.turn import resolve_damage_over_time, resolve_defense, resolve_turn


class CombatTests(unittest.TestCase):
    def test_calculate_damage(self) -> None:
        damage = calculate_damage(10, 3, "none", "physical", {})

        self.assertGreaterEqual(damage, 1, f"expected damage >= 1, got {damage}")

    def test_calculate_damage_with_critical(self) -> None:
        base_damage = 10

        no_crit = calculate_damage_with_critical(base_damage, 10)
        self.assertEqual(no_crit, base_damage, f"expected no crit at 10%, got {no_crit}")

        with_crit = calculate_damage_with_critical(base_damage, 25)
        expected_crit = base_damage + (base_damage // 2)
        self.assertEqual(with_crit, expected_crit, f"expected crit damage {expected_crit}, got {with_crit}")

    def test_get_move(self) -> None:
        move = get_move("fireball")

        self.assertIsNotNone(move, "expected to find fireball move")
        self.assertEqual(move.name, "Fireball")
        self.assertEqual(move.mana_cost, 15, f"expected mana cost 15, got {move.mana_cost}")

    def test_can_cast(self) -> None:
        move = get_move("fireball")

        self.assertFalse(can_cast(14, move), "expected to not be able to cast with 14 MP")
        self.assertTrue(can_cast(15, move), "expected to be able to cast with 15 MP")
        self.assertTrue(can_cast(20, move), "expected to be able to cast with 20 MP")

    def test_is_physical_move(self) -> None:
        slash = get_move("slash")
        fireball = get_move("fireball")

        self.assertTrue(is_physical_move(slash), "expected slash to be physical")
        self.assertFalse(is_physical_move(fireball), "expected fireball to not be physical")

    def test_resolve_turn(self) -> None:
        move = get_move("slash")

        result = resolve_turn(8, 10, 2, {}, {}, move)

        self.assertGreaterEqual(result.damage, 1, f"expected damage >= 1, got {result.damage}")
        self.assertTrue(result.hit, "expected turn to hit")

    def test_resolve_turn_stunned(self) -> None:
        attacker_status = {"stunned": 1}
        move = get_move("slash")

        result = resolve_turn(8, 10, 2, attacker_status, {}, move)

        self.assertFalse(result.hit, "expected stunned attacker to miss")
        self.assertEqual(result.damage, 0, "expected no damage from stunned attacker")

    def test_resolve_damage_over_time(self) -> None:
        status = {"burning": 1}

        total_damage, messages = resolve_damage_over_time(status)

        self.assertEqual(total_damage, 4, f"expected 4 damage from burn, got {total_damage}")
        self.assertNotEqual(len(messages), 0, "expected messages from DoT")

    def test_apply_effect(self) -> None:
        target_status: dict[str, int] = {}
        move = get_move("fireball")

        # Simulate applying the effect from the move
        if move.applies_effect != "":
            target_status[move.applies_effect] = move.effect_duration

        self.assertIn("burning", target_status, "expected burning effect to be applied")

    def test_new_actions(self) -> None:
        attack = new_attack_action("Hero", "Goblin", "slash")
        self.assertEqual(attack.action_type, ACTION_ATTACK)

        defend = new_defend_action("Hero")
        self.assertEqual(defend.action_type, ACTION_DEFEND)

        cast = new_cast_action("Mage", "Goblin", "fireball")
        self.assertEqual(cast.action_type, ACTION_CAST)

    def test_resolve_defense(self) -> None:
        base_damage = 20
        defense = 6

        final_damage = resolve_defense(base_damage, defense)

        self.assertLess(
            final_damage, base_damage, f"expected defense to reduce damage, got {final_damage} from {base_damage}"
        )
        self.assertGreaterEqual(final_damage, 1, f"expected minimum damage of 1, got {final_damage}")

    def test_damage_minimum(self) -> None:
        # Test that damage never goes below 1
        damage = calculate_damage(1, 100, "none", "physical", {})

        self.assertGreaterEqual(damage, 1, f"expected minimum damage 1, got {damage}")


if __name__ == "__main__":
    unittest.main()
