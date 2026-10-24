"""Evidence for REQ-0: what a message is, and that it does not change."""

import dataclasses

import pytest

from guard import Message, SecurityLevel


@pytest.mark.req("REQ-0")
def test_exactly_three_security_levels():
    assert {level.value for level in SecurityLevel} == {"Public", "Restricted", "Critical"}


@pytest.mark.req("REQ-0")
def test_unknown_level_is_rejected():
    with pytest.raises(ValueError):
        SecurityLevel("Secret")


@pytest.mark.req("REQ-0")
def test_level_must_be_a_security_level():
    with pytest.raises(TypeError):
        Message("Public", 1)  # type: ignore[arg-type]


@pytest.mark.req("REQ-0")
def test_payload_must_be_an_integer():
    with pytest.raises(TypeError):
        Message(SecurityLevel.PUBLIC, "42")  # type: ignore[arg-type]


@pytest.mark.req("REQ-0")
def test_message_does_not_change_after_creation():
    message = Message(SecurityLevel.PUBLIC, 42)
    with pytest.raises(dataclasses.FrozenInstanceError):
        message.payload = 43  # type: ignore[misc]
