"""Утилиты для фильтрации сообщений."""
from constants.bad_words import BAD_WORDS


def contains_bad_words(text: str) -> bool:
    """Проверка на запрещенные слова."""
    text_lower = text.lower()
    return any(bad_word in text_lower for bad_word in BAD_WORDS)
