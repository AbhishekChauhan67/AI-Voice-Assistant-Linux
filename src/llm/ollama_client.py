import logging
import time

from ollama import chat
from ollama._types import Message


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


def _request_chat(model: str, messages: list[Message]):
    return chat(model=model, messages=messages)

class LocalLLM:
    def __init__(
        self,
        model: str = "qwen3:1.7b",
        system_prompt: str = "You are a helpful voice assistant. Gives Answer very quickly.",
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
            response = _request_chat(self.model, self.messages)
            
            elapsed = time.perf_counter() - start_time
            
            

            logger.info("[LLM] Completed in %.2f seconds", elapsed)

            message = response["message"]
            answer = message.get("content", "")

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