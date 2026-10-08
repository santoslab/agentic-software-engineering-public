"""Computer opponents (contracts/opponent.md).

This is the opponent module's public API.
"""

from .base import Opponent
from .random_opponent import RandomOpponent

__all__ = ["Opponent", "RandomOpponent"]
