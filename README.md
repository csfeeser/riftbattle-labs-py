# RiftBattle: A Python Combat Game Engine

RiftBattle is a turn-based combat game engine written in Python. This codebase is designed as a teaching resource for professional software development workflows: investigation, debugging, code review, and shipping practices. It is the Python twin of the Go repo `riftbattle-labs`, with the same packages, the same planted problems, and the same branches.

## What Is RiftBattle?

A combat game where characters engage in turn-based battles. Features include:
- **Character Progression:** Leveling system with experience points, stat growth, and skill unlocks
- **Combat System:** Turn-based damage calculation with elemental effects and critical strikes
- **Status Effects:** Poison, burn, stun, and other effects that persist across turns
- **Equipment System:** Weapons and armor with rarity-based stat bonuses
- **Inventory Management:** Item collection, consumption, and effect management
- **Game Modes:** Training, ranked, story, and arena modes with different rules
- **Combat Logging:** Full action history

## Codebase Overview

**Metrics:**
- About 2,200 lines of code (2,870 with tests)
- 9 packages
- 56 tests
- Pure Python 3.10+ (standard library only)

**Package Structure:**

```
riftbattle-labs-py/
├── fighters/       # Character data, progression, stats, leveling
├── equipment/      # Equipment items, rarity, bonuses, slot management
├── items/          # Consumables (potions, antidotes), inventory, healing
├── effects/        # Status effects (poison, burn, stun), damage-over-time
├── combat/         # Damage calculation, moves, turn resolution
├── game/           # Game state and battle management
├── combatlog/      # Combat action logging and export
├── modes/          # Game mode definitions and multipliers
├── utils/          # Math utilities, validation helpers
└── main.py         # Entry point (plus a small standalone demo engine in the root files)
```

**Differences from the Go repo (Python naming rules):**
- `combatlog/` replaces Go's `logging/` (a top-level `logging` package would shadow Python's standard library).
- `utils/math_utils.py` replaces `utils/math.go`, and root `status_effects.py` replaces root `effects.go` (a root `effects.py` would collide with the `effects/` package).
- `models.py` replaces root `types.go`.
- Healing functions take a small `HealTarget` object instead of Go pointers (Python integers are immutable).

### Setup
```bash
git clone https://github.com/csfeeser/riftbattle-labs-py.git
cd riftbattle-labs-py

# Verify the main branch works
git checkout main
python main.py
python -m unittest
```

### Checking Out Different Branches
```bash
git checkout main                    # Labs 1 & 3
git checkout lab-2-with-bug          # Lab 2 (bug hunt)
git checkout review-branch           # Skills and loops lab
git checkout feature/stun-system     # Code review
git checkout feature/equipment-system  # Shipping workflow
```

## Running Tests

```bash
# All tests
python -m unittest

# Specific package
python -m unittest discover -s items -t .

# Specific test
python -m unittest items.test_items.ItemsTests.test_healing_potion_poisoned_character_cannot_heal

# Lab 2 specific (see expected failures)
python -m unittest -k poison
```

## Architecture Notes

**Intentional Fragility** (for learning):
- The main branch deliberately couples packages to teach modularity
- Some functions are defined but never used (dead code)
- String-based effect management instead of typed constants
- Missing validation on critical functions
- Naming inconsistencies between modules

This fragility is **intentional** and designed to teach investigation skills. Production code should not follow these patterns.
