from dataclasses import dataclass

# Item types
ITEM_TYPE_CONSUMABLE = "consumable"
ITEM_TYPE_EQUIPMENT = "equipment"
ITEM_TYPE_QUEST = "quest"


@dataclass
class Item:
    """An item in the game."""

    id: str
    name: str
    item_type: str
    quantity: int
    value: int  # Gold value
    max_stack: int  # Maximum stack size


@dataclass
class ConsumableItem(Item):
    """A consumable item."""

    effect_type: str = ""  # "heal", "mana", "poison_cure", "buff"
    effect_value: int = 0
    effect_duration: int = 0
    rarity: str = ""

    def can_stack(self) -> bool:
        """Check if two items can stack."""
        return self.quantity < self.max_stack

    def add_to_stack(self, quantity: int) -> int:
        """Add quantity to the item and return the overflow."""
        available_space = self.max_stack - self.quantity
        to_add = quantity
        if quantity > available_space:
            to_add = available_space
        self.quantity += to_add
        return quantity - to_add

    def remove_from_stack(self, quantity: int) -> bool:
        """Remove quantity from the item."""
        if self.quantity >= quantity:
            self.quantity -= quantity
            return True
        return False


def new_healing_potion(quantity: int) -> ConsumableItem:
    """Create a healing potion."""
    return ConsumableItem(
        id="healing_potion",
        name="Healing Potion",
        item_type=ITEM_TYPE_CONSUMABLE,
        quantity=quantity,
        value=50,
        max_stack=99,
        effect_type="heal",
        effect_value=12,
        rarity="common",
    )


def new_greater_healing_potion(quantity: int) -> ConsumableItem:
    """Create a greater healing potion."""
    return ConsumableItem(
        id="greater_healing_potion",
        name="Greater Healing Potion",
        item_type=ITEM_TYPE_CONSUMABLE,
        quantity=quantity,
        value=150,
        max_stack=50,
        effect_type="heal",
        effect_value=25,
        rarity="uncommon",
    )


def new_mana_potion(quantity: int) -> ConsumableItem:
    """Create a mana potion."""
    return ConsumableItem(
        id="mana_potion",
        name="Mana Potion",
        item_type=ITEM_TYPE_CONSUMABLE,
        quantity=quantity,
        value=75,
        max_stack=99,
        effect_type="mana",
        effect_value=15,
        rarity="common",
    )


def new_antidote(quantity: int) -> ConsumableItem:
    """Create an antidote for poison."""
    return ConsumableItem(
        id="antidote",
        name="Antidote",
        item_type=ITEM_TYPE_CONSUMABLE,
        quantity=quantity,
        value=100,
        max_stack=30,
        effect_type="poison_cure",
        effect_value=1,
        rarity="common",
    )
