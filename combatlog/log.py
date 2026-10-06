from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

# Log levels (string-based, like the rest of the codebase)
LEVEL_DEBUG = "debug"
LEVEL_INFO = "info"
LEVEL_WARNING = "warning"
LEVEL_ERROR = "error"


@dataclass
class LogEntry:
    """A single log entry."""

    timestamp: datetime
    level: str
    message: str
    context: dict[str, Any] = field(default_factory=dict)


class CombatLogger:
    """Manages combat logging."""

    def __init__(self) -> None:
        self.entries: list[LogEntry] = []
        self.active = True

    def log(self, level: str, message: str) -> None:
        """Add a log entry."""
        if not self.active:
            return

        entry = LogEntry(timestamp=datetime.now(), level=level, message=message)
        self.entries.append(entry)

    def log_action(self, actor: str, action: str, target: str) -> None:
        """Log a combat action."""
        message = actor + " uses " + action + " on " + target
        self.log(LEVEL_INFO, message)

    def log_damage(self, attacker: str, defender: str, amount: int) -> None:
        """Log damage dealt."""
        # Magic string - intentional fragility
        message = attacker + " deals " + itoa(amount) + " damage to " + defender
        self.log(LEVEL_INFO, message)

    def log_healing(self, healer: str, target: str, amount: int) -> None:
        """Log healing applied."""
        message = healer + " heals " + target + " for " + itoa(amount) + " HP"
        self.log(LEVEL_INFO, message)

    def log_status_effect(self, target: str, effect: str) -> None:
        """Log status effect application."""
        message = target + " is now " + effect
        self.log(LEVEL_INFO, message)

    def clear(self) -> None:
        """Clear all log entries."""
        self.entries = []

    def get_entries(self) -> list[LogEntry]:
        """Return all log entries."""
        return self.entries

    def get_entries_since(self, since: datetime) -> list[LogEntry]:
        """Return entries after a certain time."""
        result: list[LogEntry] = []
        for entry in self.entries:
            if entry.timestamp > since:
                result.append(entry)
        return result

    def export(self) -> list[str]:
        """Export logs as strings."""
        result: list[str] = []
        for entry in self.entries:
            result.append(
                entry.timestamp.strftime("%H:%M:%S") + " [" + entry.level + "] " + entry.message
            )
        return result


def itoa(value: int) -> str:
    """Convert int to string - copied from items package (code duplication issue)."""
    if value == 0:
        return "0"
    if value < 0:
        return "-" + itoa(-value)

    result = ""
    while value > 0:
        result = chr(ord("0") + value % 10) + result
        value //= 10
    return result
