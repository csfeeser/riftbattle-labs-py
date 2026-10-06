from typing import Optional

from items.item import ConsumableItem


class Inventory:
    """A fighter's inventory."""

    def __init__(self, max_slots: int) -> None:
        self.id = "inv_1"
        self.slots: list[ConsumableItem] = []
        self.max_slots = max_slots
        self.weight = 0
        self.max_weight = 100

    def add_item(self, item: ConsumableItem) -> bool:
        """Add an item to inventory."""
        # Missing validation - intentional fragility
        # Should check:
        # 1. max_slots limit
        # 2. Weight limit
        # 3. Stack size limits

        self.slots.append(item)
        self.weight += int(item.value / 10)  # Rough weight calculation
        return True

    def remove_item(self, index: int) -> bool:
        """Remove an item from inventory."""
        if index < 0 or index >= len(self.slots):
            return False
        del self.slots[index]
        return True

    def get_item_by_id(self, item_id: str) -> Optional[ConsumableItem]:
        """Find an item by ID."""
        for item in self.slots:
            if item.id == item_id:
                return item
        return None

    def count_item(self, item_id: str) -> int:
        """Count how many of an item type we have."""
        item = self.get_item_by_id(item_id)
        if item is None:
            return 0
        return item.quantity

    def is_full(self) -> bool:
        """Check if inventory is full."""
        return len(self.slots) >= self.max_slots
