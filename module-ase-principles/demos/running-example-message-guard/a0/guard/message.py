"""The message that crosses the guard (REQ-0): a security level and an integer payload."""

from dataclasses import dataclass
from enum import Enum


class SecurityLevel(Enum):
    """The marking that says how sensitive a message is, in increasing order."""

    PUBLIC = "Public"
    RESTRICTED = "Restricted"
    CRITICAL = "Critical"


@dataclass(frozen=True)
class Message:
    """A message: its security level and its payload. Frozen, so it cannot change (REQ-0)."""

    level: SecurityLevel
    payload: int

    def __post_init__(self) -> None:
        if not isinstance(self.level, SecurityLevel):
            raise TypeError(f"level must be a SecurityLevel, not {type(self.level).__name__}")
        if not isinstance(self.payload, int):
            raise TypeError(f"payload must be an int, not {type(self.payload).__name__}")
