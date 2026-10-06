from dataclasses import dataclass, field

# Rarity levels
RARITY_COMMON = "common"
RARITY_UNCOMMON = "uncommon"
RARITY_RARE = "rare"
RARITY_EPIC = "epic"
RARITY_LEGENDARY = "legendary"

# Equipment types
TYPE_WEAPON = "weapon"
TYPE_ARMOR = "armor"
TYPE_ACCESSORY = "accessory"

# Equip slots
SLOT_MAIN_HAND = "main_hand"
SLOT_OFF_HAND = "off_hand"
SLOT_HEAD = "head"
SLOT_CHEST = "chest"
SLOT_LEGS = "legs"
SLOT_FEET = "feet"
SLOT_ACCESSORY = "accessory"


@dataclass
class Equipment:
    """An equippable item."""

    name: str
    equipment_type: str
    slot: str
    rarity: str
    required_level: int
    id: str = ""
    power_bonus: int = 0
    defense_bonus: int = 0
    agility_bonus: int = 0
    spirit_bonus: int = 0
    crit_bonus: int = 0
    effect_resist: dict[str, int] = field(default_factory=dict)  # e.g. "poison": 25
    weapon_class: str = ""  # For weapons: "sword", "staff", "dagger"
    damage_type: str = ""  # For weapons: "physical", "magic", "special"
    armor_class: str = ""  # For armor: "light", "medium", "heavy"
    special_ability: str = ""  # Rare+ equipment might have special abilities

    def get_rarity_bonus(self) -> float:
        """Return the stat multiplier for this equipment's rarity."""
        if self.rarity == RARITY_COMMON:
            return 1.0
        if self.rarity == RARITY_UNCOMMON:
            return 1.15
        if self.rarity == RARITY_RARE:
            return 1.35
        if self.rarity == RARITY_EPIC:
            return 1.6
        if self.rarity == RARITY_LEGENDARY:
            return 2.0
        return 1.0

    def get_total_power_bonus(self) -> int:
        """Calculate power bonus with rarity multiplier."""
        return int(float(self.power_bonus) * self.get_rarity_bonus())

    def can_equip_at(self, level: int) -> bool:
        """Check if equipment can be equipped at a given level."""
        return level >= self.required_level

    def add_effect_resistance(self, effect: str, resistance: int) -> None:
        """Add resistance to an effect."""
        self.effect_resist[effect] = resistance

    def get_effect_resistance(self, effect: str) -> int:
        """Return the resistance to an effect."""
        return self.effect_resist.get(effect, 0)


def new_weapon(
    name: str, weapon_class: str, damage_type: str, power: int, level: int, rarity: str
) -> Equipment:
    """Create a new weapon."""
    return Equipment(
        name=name,
        equipment_type=TYPE_WEAPON,
        slot=SLOT_MAIN_HAND,
        rarity=rarity,
        required_level=level,
        power_bonus=power,
        weapon_class=weapon_class,
        damage_type=damage_type,
    )


def new_armor(
    name: str, slot: str, armor_class: str, defense: int, spirit: int, level: int, rarity: str
) -> Equipment:
    """Create a new armor piece."""
    return Equipment(
        name=name,
        equipment_type=TYPE_ARMOR,
        slot=slot,
        rarity=rarity,
        required_level=level,
        defense_bonus=defense,
        spirit_bonus=spirit,
        armor_class=armor_class,
    )


def new_accessory(
    name: str, power: int, defense: int, agility: int, spirit: int, level: int, rarity: str
) -> Equipment:
    """Create a new accessory."""
    return Equipment(
        name=name,
        equipment_type=TYPE_ACCESSORY,
        slot=SLOT_ACCESSORY,
        rarity=rarity,
        required_level=level,
        power_bonus=power,
        defense_bonus=defense,
        agility_bonus=agility,
        spirit_bonus=spirit,
    )
