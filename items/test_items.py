import unittest

from items.healing import (
    HealTarget,
    apply_healing,
    apply_poison_cure,
    restore_mana,
    use_greater_healing_potion,
    use_healing_potion,
)
from items.inventory import Inventory
from items.item import new_healing_potion


class ItemsTests(unittest.TestCase):
    def test_healing_potion_basic(self) -> None:
        target = HealTarget("Hero", hp=20, max_hp=50)

        healed = apply_healing(target, 12)

        self.assertEqual(target.hp, 32, f"expected HP 32, got {target.hp}")
        self.assertEqual(healed, 12, f"expected 12 healing, got {healed}")

    def test_healing_potion_healthy_character_can_heal(self) -> None:
        target = HealTarget("Hero", hp=15, max_hp=30)

        result = use_healing_potion(target)

        self.assertGreater(target.hp, 15, "expected healing to increase HP")
        self.assertEqual(result, "Hero drinks a potion and restores 12 HP.")

    def test_healing_potion_poisoned_character_cannot_heal(self) -> None:
        target = HealTarget("Hero", hp=15, max_hp=30, status={"poisoned": 2})

        healed = apply_healing(target, 12)

        self.assertEqual(
            target.hp, 15, f"expected no healing while poisoned, HP changed from 15 to {target.hp}"
        )
        self.assertEqual(healed, 0, f"expected 0 healing returned, got {healed}")

        result = use_healing_potion(target)
        self.assertEqual(result, "Hero cannot heal while poisoned.")

    def test_healing_potion_poison_wearing_off_allows_healing(self) -> None:
        target = HealTarget("Hero", hp=15, max_hp=30, status={"poisoned": 1})

        # Simulate poison wearing off
        del target.status["poisoned"]

        healed = apply_healing(target, 12)

        self.assertGreater(target.hp, 15, "expected healing to work after poison expires")
        self.assertEqual(healed, 12, f"expected 12 healing, got {healed}")

    def test_healing_potion_multiple_poison_still_blocks_healing(self) -> None:
        target = HealTarget("Hero", hp=15, max_hp=30, status={"poisoned": 3})

        healed = apply_healing(target, 12)

        self.assertEqual(target.hp, 15, "expected no healing with multiple poisons")
        self.assertEqual(healed, 0, f"expected 0 healing, got {healed}")

    def test_greater_healing_potion(self) -> None:
        target = HealTarget("Mage", hp=10, max_hp=50)

        result = use_greater_healing_potion(target)

        self.assertEqual(target.hp, 35, f"expected HP 35, got {target.hp}")
        self.assertEqual(result, "Mage drinks a potion and restores 25 HP.")

    def test_restore_mana(self) -> None:
        target = HealTarget("Mage", hp=30, max_hp=30, mp=5, max_mp=50)

        restored = restore_mana(target, 15)

        self.assertEqual(target.mp, 20, f"expected MP 20, got {target.mp}")
        self.assertEqual(restored, 15, f"expected 15 restoration, got {restored}")

    def test_healing_clamps_to_max_hp(self) -> None:
        target = HealTarget("Hero", hp=40, max_hp=50)

        apply_healing(target, 100)

        self.assertEqual(target.hp, 50, f"expected HP clamped to 50, got {target.hp}")

    def test_inventory_add_item(self) -> None:
        inv = Inventory(10)
        potion = new_healing_potion(5)

        inv.add_item(potion)

        self.assertEqual(len(inv.slots), 1, f"expected 1 item in inventory, got {len(inv.slots)}")

    def test_inventory_get_item(self) -> None:
        inv = Inventory(10)
        potion = new_healing_potion(5)
        inv.add_item(potion)

        found = inv.get_item_by_id("healing_potion")

        self.assertIsNotNone(found, "expected to find healing potion")
        self.assertEqual(found.quantity, 5, f"expected 5 potions, got {found.quantity}")

    def test_poison_cure(self) -> None:
        status = {"poisoned": 2}

        cured = apply_poison_cure(status)

        self.assertTrue(cured, "expected poison to be cured")
        self.assertNotIn("poisoned", status, "expected poisoned status to be removed")

    def test_new_healing_potion(self) -> None:
        potion = new_healing_potion(3)

        self.assertEqual(potion.effect_value, 12, f"expected healing value 12, got {potion.effect_value}")
        self.assertEqual(potion.max_stack, 99, f"expected max stack 99, got {potion.max_stack}")

    def test_consumable_stack(self) -> None:
        potion = new_healing_potion(50)

        self.assertTrue(potion.can_stack(), "expected healing potion to be stackable")

        potion.quantity = 99
        self.assertFalse(potion.can_stack(), "expected healing potion to not be stackable at max")


if __name__ == "__main__":
    unittest.main()
