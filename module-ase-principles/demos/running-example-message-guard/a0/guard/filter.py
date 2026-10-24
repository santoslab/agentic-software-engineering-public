"""The filter stage: pass or drop a message by its security level (REQ-1 to REQ-3)."""

from guard.message import Message, SecurityLevel


def filter_message(message: Message) -> Message | None:
    """Return the message unchanged if it may leave the enclave, or None if it is dropped."""
    if message.level is SecurityLevel.CRITICAL:
        return None  # REQ-1
    return message  # REQ-2, REQ-3
