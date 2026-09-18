import logging
import time

from ollama import chat
from ollama._types import Message


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

class LocalLLM:
    def __init__(
        self,
        model: str = "qwen3:4b",
        system_prompt: str = "You are a helpful voice assistant. Gives Answer very quickly.",
    ) -> None:
        self.model = model
        self.system_prompt = system_prompt
        self.thinking = ""

        self.messages: list[Message] = [
            Message(
                role="system",
                content=system_prompt,
            )
        ]

    def ask(self, text: str) -> str:
        
        logger.info("[LLM] Starting...")
        logger.info("[LLM] User: %s", text)
        
        start_time = time.perf_counter()
        
        self.messages.append(
            Message(
                role="user",
                content=text,
            )
        )
        
        try: 
            response = chat(
                model=self.model,
                messages=self.messages,
                think=True,
            )
            
            elapsed = time.perf_counter() - start_time

            logger.info("[LLM] Completed in %.2f seconds", elapsed)

            message = response["message"]
            self.thinking = message.get("thinking", "")
            answer = message["content"]

            self.messages.append(
                Message(
                    role="assistant",
                    content=answer,
                )
            )

            logger.info("[LLM] Assistant: %s", answer)
            
            return answer
        except Exception:
            logger.error("[LLM] Failed.")
            raise
        finally:
            logger.info("[LLM] Terminated.")

    def clear_history(self) -> None:
        self.messages = [
            Message(
                role="system",
                content=self.system_prompt,
            )
        ]
        
if __name__ == "__main__":
    llm = LocalLLM()
    
    while True:
        query = input("Enter Query: ")
        
        if query == "exit":
            break
        llm.ask(query)