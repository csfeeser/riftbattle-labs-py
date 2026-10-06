import unittest

from equipment.equipment import RARITY_COMMON, RARITY_EPIC, RARITY_LEGENDARY, RARITY_RARE
from equipment.rarity_bonuses import apply_rarity_bonus, get_rarity_bonus


class RarityBonusTests(unittest.TestCase):
    def test_get_rarity_bonus(self) -> None:
        bonus = get_rarity_bonus(RARITY_COMMON)
        self.assertEqual(bonus.power_bonus, 1.0, f"expected common power bonus 1.0, got {bonus.power_bonus}")

        legendary_bonus = get_rarity_bonus(RARITY_LEGENDARY)
        self.assertEqual(
            legendary_bonus.power_bonus, 2.0, f"expected legendary power bonus 2.0, got {legendary_bonus.power_bonus}"
        )

        epic_bonus = get_rarity_bonus(RARITY_EPIC)
        self.assertEqual(epic_bonus.crit_bonus, 10, f"expected epic crit bonus 10, got {epic_bonus.crit_bonus}")

    def test_apply_rarity_bonus(self) -> None:
        common_result = apply_rarity_bonus(100, RARITY_COMMON, "power")
        self.assertEqual(common_result, 100, f"expected common bonus to be 1.0x, got {common_result}")

        rare_result = apply_rarity_bonus(100, RARITY_RARE, "power")
        self.assertEqual(rare_result, 135, f"expected rare bonus 135, got {rare_result}")  # 100 * 1.35

        legendary_result = apply_rarity_bonus(100, RARITY_LEGENDARY, "spirit")
        self.assertEqual(legendary_result, 200, f"expected legendary bonus 200, got {legendary_result}")  # 100 * 2.0

    def test_get_rarity_bonus_unknown(self) -> None:
        # Passing invalid rarity should return common
        bonus = get_rarity_bonus("invalid")
        self.assertEqual(bonus.power_bonus, 1.0, "expected invalid rarity to return common bonus")


if __name__ == "__main__":
    unittest.main()
