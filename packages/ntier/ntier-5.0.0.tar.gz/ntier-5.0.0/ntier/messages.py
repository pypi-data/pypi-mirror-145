"""Contains the Messages data structure."""
from typing import List, Mapping, MutableMapping, Optional

_GENERAL_SUBJECT = ""

MessageData = Mapping[str, List[str]]


class Messages:
    """Contains a mapping of subjects to a list of messages."""

    def __init__(self, data: Optional[MessageData] = None) -> None:
        self._data: MutableMapping[str, List[str]] = {**data} if data else {}

    def __bool__(self):
        return self.has_messages

    @property
    def has_messages(self) -> bool:
        return bool(self._data)

    @property
    def data(self) -> MessageData:
        return self._data

    @property
    def general_messages(self) -> List[str]:
        return self._data.get(_GENERAL_SUBJECT, [])

    def add_message(self, subject: str, message: str) -> "Messages":
        if subject not in self._data:
            self._data[subject] = []
        self._data[subject].append(message)
        return self

    def add_general_message(self, message: str) -> "Messages":
        return self.add_message(_GENERAL_SUBJECT, message)

    def has_message_for(self, subject: str) -> bool:
        return subject in self._data

    def has_general_message(self) -> bool:
        return self.has_message_for(_GENERAL_SUBJECT)

    def merge(self, message_data: MessageData) -> "Messages":
        for (key, values) in message_data.items():
            for value in values:
                self.add_message(key, value)
        return self

    def union(self, other: "Messages") -> "Messages":
        messages = Messages()
        messages.merge(self.data)
        messages.merge(other.data)
        return messages
