import unittest

from equipment.equipment import (
    RARITY_COMMON,
    RARITY_EPIC,
    RARITY_LEGENDARY,
    RARITY_RARE,
    SLOT_ACCESSORY,
    SLOT_CHEST,
    SLOT_MAIN_HAND,
    new_accessory,
    new_armor,
    new_weapon,
)
from equipment.stats import EquipmentSet


class EquipmentTests(unittest.TestCase):
    def test_new_weapon(self) -> None:
        sword = new_weapon("Iron Sword", "sword", "physical", 8, 1, RARITY_COMMON)

        self.assertEqual(sword.name, "Iron Sword")
        self.assertEqual(sword.power_bonus, 8, f"expected power bonus 8, got {sword.power_bonus}")
        self.assertEqual(sword.slot, SLOT_MAIN_HAND)

    def test_equipment_rarity(self) -> None:
        common = new_weapon("Common Sword", "sword", "physical", 10, 1, RARITY_COMMON)
        rare = new_weapon("Rare Sword", "sword", "physical", 10, 5, RARITY_RARE)
        legendary = new_weapon("Legendary Sword", "sword", "physical", 10, 20, RARITY_LEGENDARY)

        self.assertEqual(common.get_rarity_bonus(), 1.0)
        self.assertEqual(rare.get_rarity_bonus(), 1.35)
        self.assertEqual(legendary.get_rarity_bonus(), 2.0)

        rare_bonus = rare.get_total_power_bonus()
        # Rare items get 35% bonus to power
        self.assertEqual(rare_bonus, 13)  # 10 * 1.35 = 13.5, cast to int = 13

    def test_equipment_set(self) -> None:
        equipment_set = EquipmentSet()
        sword = new_weapon("Iron Sword", "sword", "physical", 8, 1, RARITY_COMMON)
        armor = new_armor("Iron Chest", "chest", "heavy", 6, 0, 1, RARITY_COMMON)

        equipment_set.equip(sword)
        equipment_set.equip(armor)

        self.assertIs(equipment_set.get_equipped(SLOT_MAIN_HAND), sword, "expected sword in main hand")
        self.assertIs(equipment_set.get_equipped(SLOT_CHEST), armor, "expected armor in chest")

    def test_calculate_total_bonuses(self) -> None:
        equipment_set = EquipmentSet()
        sword = new_weapon("Iron Sword", "sword", "physical", 8, 1, RARITY_COMMON)
        armor = new_armor("Iron Chest", "chest", "heavy", 6, 2, 1, RARITY_COMMON)

        equipment_set.equip(sword)
        equipment_set.equip(armor)

        bonus = equipment_set.calculate_total_bonuses()

        self.assertEqual(bonus.power_bonus, 8, f"expected power bonus 8, got {bonus.power_bonus}")
        self.assertEqual(bonus.defense_bonus, 6, f"expected defense bonus 6, got {bonus.defense_bonus}")
        self.assertEqual(bonus.spirit_bonus, 2, f"expected spirit bonus 2, got {bonus.spirit_bonus}")

    def test_equipment_can_equip_at(self) -> None:
        sword = new_weapon("Iron Sword", "sword", "physical", 8, 5, RARITY_COMMON)

        self.assertFalse(sword.can_equip_at(3), "expected sword to not be equippable at level 3")
        self.assertTrue(sword.can_equip_at(5), "expected sword to be equippable at level 5")
        self.assertTrue(sword.can_equip_at(10), "expected sword to be equippable at level 10")

    def test_effect_resistance(self) -> None:
        armor = new_armor("Fire Resistant Armor", "chest", "heavy", 6, 0, 1, RARITY_COMMON)
        armor.add_effect_resistance("burning", 25)
        armor.add_effect_resistance("poison", 15)

        self.assertEqual(armor.get_effect_resistance("burning"), 25)
        self.assertEqual(armor.get_effect_resistance("poison"), 15)
        self.assertEqual(armor.get_effect_resistance("frozen"), 0)

    def test_set_bonus(self) -> None:
        equipment_set = EquipmentSet()

        # Add 4 epic items in different slots
        weapon = new_weapon("Epic Sword", "sword", "physical", 10, 1, RARITY_EPIC)
        equipment_set.equip(weapon)

        head = new_armor("Epic Crown", "head", "light", 5, 3, 1, RARITY_EPIC)
        equipment_set.equip(head)

        chest = new_armor("Epic Chestplate", "chest", "heavy", 8, 2, 1, RARITY_EPIC)
        equipment_set.equip(chest)

        legs = new_armor("Epic Leggings", "legs", "heavy", 6, 1, 1, RARITY_EPIC)
        equipment_set.equip(legs)

        self.assertTrue(equipment_set.has_set_bonus(), "expected set bonus with 4 epic items")

        multiplier = equipment_set.get_set_bonus_multiplier()
        self.assertEqual(multiplier, 1.2, f"expected epic set bonus 1.2, got {multiplier}")

    def test_accessory(self) -> None:
        ring = new_accessory("Ring of Power", 5, 2, 3, 4, 1, RARITY_COMMON)

        self.assertEqual(ring.slot, SLOT_ACCESSORY)
        self.assertEqual(ring.power_bonus, 5, f"expected power bonus 5, got {ring.power_bonus}")


if __name__ == "__main__":
    unittest.main()
