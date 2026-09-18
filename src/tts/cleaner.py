import logging
import re
import unicodedata


logger = logging.getLogger(__name__)


def clean_for_piper(text: str) -> str:
    original_length = len(text)
    # Remove emojis and other non-ASCII characters
    text = text.encode("ascii", "ignore").decode("ascii")

    # Remove Markdown emphasis
    text = re.sub(r"[*_~`]", "", text)

    # Remove URLs
    text = re.sub(r"https?://\S+|www\.\S+", "", text)

    # Keep letters, numbers, basic punctuation
    text = re.sub(r"[^a-zA-Z0-9\s.,!?;:'\"()\-]", "", text)

    # Remove multiple spaces
    text = re.sub(r"\s+", " ", text)

    cleaned_text = text.strip()
    logger.debug(
        "Cleaned Piper text from %d to %d characters",
        original_length,
        len(cleaned_text),
    )
    return cleaned_text