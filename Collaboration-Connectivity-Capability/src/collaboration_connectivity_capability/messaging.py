"""Local, inspectable project-to-project message exchange foundation."""

from __future__ import annotations

from dataclasses import replace

from .enums import MessageStatus
from .models import CollaborationMessage, MessageResult, utc_now


class InMemoryMessageBus:
    def __init__(self) -> None:
        self._messages: dict[str, tuple[CollaborationMessage, MessageStatus]] = {}

    def send(self, message: CollaborationMessage) -> MessageResult:
        if message.expires_at is not None and message.expires_at <= utc_now():
            self._messages[message.message_id] = (message, MessageStatus.EXPIRED)
            return MessageResult(message.message_id, MessageStatus.EXPIRED, False, "MESSAGE_EXPIRED", "Message has expired")
        if not message.source.strip() or not message.target.strip() or not message.message_type.strip():
            self._messages[message.message_id] = (message, MessageStatus.REJECTED)
            return MessageResult(message.message_id, MessageStatus.REJECTED, False, "INVALID_REQUEST", "Message identity is incomplete")
        self._messages[message.message_id] = (message, MessageStatus.SENT)
        return MessageResult(message.message_id, MessageStatus.SENT, True, message="Message accepted")

    def receive(self, target: str) -> tuple[CollaborationMessage, ...]:
        delivered: list[CollaborationMessage] = []
        for message_id, (message, status) in list(self._messages.items()):
            if message.target == target and status == MessageStatus.SENT:
                self._messages[message_id] = (message, MessageStatus.DELIVERED)
                delivered.append(message)
        return tuple(sorted(delivered, key=lambda item: (-item.priority, item.created_at)))

    def status(self, message_id: str) -> MessageStatus | None:
        item = self._messages.get(message_id)
        return item[1] if item else None

    def mark_failed(self, message_id: str) -> MessageResult:
        item = self._messages.get(message_id)
        if item is None:
            return MessageResult(message_id, MessageStatus.FAILED, False, "INVALID_REQUEST", "Message not found")
        self._messages[message_id] = (item[0], MessageStatus.FAILED)
        return MessageResult(message_id, MessageStatus.FAILED, False, "CONNECTION_FAILED", "Message delivery failed")
