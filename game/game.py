from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from fighters.fighter import Fighter

# Game modes
MODE_TRAINING = "training"
MODE_RANKED = "ranked"
MODE_STORY = "story"
MODE_ARENA = "arena"


@dataclass
class GameState:
    """The current state of a battle."""

    id: str
    mode: str
    hero: Fighter
    enemy: Fighter
    turn: int = 0
    is_active: bool = True
    winner: Optional[Fighter] = None
    created_at: Optional[datetime] = None
    last_updated: Optional[datetime] = None
    log: list[str] = field(default_factory=list)

    def start_battle(self) -> list[str]:
        """Initialize the battle."""
        messages: list[str] = []
        messages.append("Battle started!")
        messages.append(self.hero.name + " vs " + self.enemy.name)

        # Apply training mode bonuses if applicable
        if self.mode == MODE_TRAINING:
            messages.append("[TRAINING MODE] Damage is reduced.")

        self.log.extend(messages)
        return messages

    def process_turn(self, attacker_move: str) -> list[str]:
        """Process a single turn of combat."""
        messages: list[str] = []

        if not self.is_active:
            return messages

        self.turn += 1

        # Tick status effects before turn
        self._tick_effects(self.hero, messages)
        self._tick_effects(self.enemy, messages)

        # Alternate turns between hero and enemy
        if self.turn % 2 == 1:
            messages.append(self.hero.name + " attacks with " + attacker_move)
            # Damage calculation would happen here
            messages.append(self.enemy.name + " takes damage")
        else:
            messages.append(self.enemy.name + " attacks with basic attack")
            messages.append(self.hero.name + " takes damage")

        # Check for defeat
        if self.hero.is_defeated():
            self.is_active = False
            self.winner = self.enemy
            messages.append(self.hero.name + " is defeated!")
        if self.enemy.is_defeated():
            self.is_active = False
            self.winner = self.hero
            messages.append(self.enemy.name + " is defeated!")

            # Award XP in training mode
            if self.mode == MODE_TRAINING:
                self.hero.add_xp(50)
                messages.append("Gained 50 XP (Training bonus: 1x)")
            else:
                self.hero.add_xp(30)
                messages.append("Gained 30 XP")

        self.log.extend(messages)
        self.last_updated = datetime.now()
        return messages

    def _tick_effects(self, fighter: Fighter, messages: list[str]) -> None:
        """Tick status effects for a fighter."""
        if fighter.status is None:
            return

        for effect, duration in list(fighter.status.items()):
            if duration <= 0:
                del fighter.status[effect]
                continue

            # Apply DoT damage
            if effect == "burning":
                fighter.hp -= 4
            elif effect == "poisoned":
                fighter.hp -= 3

            # Tick down duration
            fighter.status[effect] = duration - 1

    def end_battle(self) -> list[str]:
        """End the current battle."""
        messages: list[str] = []

        if self.winner is None:
            messages.append("Battle ended in draw.")
        else:
            messages.append(self.winner.name + " wins the battle!")

        self.is_active = False
        self.last_updated = datetime.now()
        self.log.extend(messages)
        return messages

    def scan_all_fighters_for_defeated(self) -> list[str]:
        """Scan entire fighter list on each turn (PERFORMANCE ISSUE)."""
        # PERFORMANCE ISSUE: Unnecessary O(n) scan on each turn
        # Should use event-driven approach: when hp <= 0, trigger cleanup immediately
        # Instead of: scan every fighter every turn
        messages: list[str] = []
        fighters = [self.hero, self.enemy]

        for f in fighters:
            if f.hp <= 0:
                messages.append(f.name + " is defeated!")
        return messages

    def resolve_turn_without_error_handling(self, attacker_move: str) -> None:
        """Resolve turn and ignore errors (ERROR HANDLING ISSUE)."""
        # ERROR HANDLING ISSUE: Ignores errors from combat resolution
        # If resolve_combat returns an error, game state could be inconsistent
        # but game continues anyway without notifying user
        _ = self._resolve_combat_with_error(attacker_move)  # ERROR DISCARDED
        # Game continues in potentially invalid state

    def _resolve_combat_with_error(self, move: str):
        """Return an error that gets ignored."""
        if self.hero is None or self.enemy is None:
            return ValueError("invalid game state")
        return None

    def get_battle_log(self) -> list[str]:
        """Return the full battle log."""
        return self.log

    def get_game_status(self) -> str:
        """Return current game status."""
        if not self.is_active:
            if self.winner is None:
                return "ended_draw"
            if self.winner is self.hero:
                return "ended_hero_win"
            return "ended_enemy_win"
        return "active"

    def apply_mode_modifiers(self) -> None:
        """Apply game mode specific rules."""
        if self.mode == MODE_TRAINING:
            # Training mode: damage reduced by 20%
            # This would be applied during damage calculation
            pass
        elif self.mode == MODE_RANKED:
            # Ranked mode: no items allowed
            pass
        elif self.mode == MODE_ARENA:
            # Arena mode: random modifiers
            pass


def new_game(hero: Fighter, enemy: Fighter, mode: str) -> GameState:
    """Create a new game session."""
    return GameState(
        id=generate_id(),
        mode=mode,
        hero=hero,
        enemy=enemy,
        turn=0,
        is_active=True,
        log=[],
        created_at=datetime.now(),
    )


def generate_id() -> str:
    """Generate a unique game ID."""
    return "game_" + datetime.now().strftime("%Y%m%d%H%M%S")


def apply_command_without_validation(gs: GameState, user_input: str) -> None:
    """Apply user command without validation (SECURITY ISSUE)."""
    # SECURITY ISSUE: No validation of user input
    # Malicious input could cause undefined behavior
    # Should validate user_input is in allowed command set before executing
    if user_input == "attack":
        pass  # Apply attack
    elif user_input == "defend":
        pass  # Apply defend
    else:
        # Unknown commands are applied anyway - this is the issue
        _ = user_input  # Silently accepts any input
