class Detect:
    def __init__(self, word: str) -> None:
        self.wake = word.strip().lower()

    def check(self, text: str) -> bool:
        text = text.strip().lower()

        return text.startswith(self.wake)