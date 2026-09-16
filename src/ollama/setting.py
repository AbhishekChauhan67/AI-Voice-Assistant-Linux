from ollama import chat
from ollama._types import Message


class LocalLLM:
    def __init__(
        self,
        model: str,
        system_prompt: str = "You are a helpful voice assistant.",
    ) -> None:
        self.model = model
        self.system_prompt = system_prompt

        self.messages: list[Message] = [
            Message(
                role="system",
                content=system_prompt,
            )
        ]

    def ask(self, text: str) -> str:
        self.messages.append(
            Message(
                role="user",
                content=text,
            )
        )

        response = chat(
            model=self.model,
            messages=self.messages,
        )

        answer = response["message"]["content"]

        self.messages.append(
            Message(
                role="assistant",
                content=answer,
            )
        )

        return answer

    def clear_history(self) -> None:
        self.messages = [
            Message(
                role="system",
                content=self.system_prompt,
            )
        ]