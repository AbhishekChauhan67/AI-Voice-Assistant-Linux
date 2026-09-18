import logging
import threading

from PySide6.QtCore import QObject, Signal, Slot

try:
	from llm.ollama_client import LocalLLM
	from stt import STT
	from stt.settings import AppConfig
	from tts.config import AUDIO_DEVICE, PIPER_MODEL
	from tts.piper import PiperTTS
except ModuleNotFoundError:
	from src.llm.ollama_client import LocalLLM
	from src.stt import STT
	from src.stt.settings import AppConfig
	from src.tts.config import AUDIO_DEVICE, PIPER_MODEL
	from src.tts.piper import PiperTTS


logger = logging.getLogger(__name__)


class AssistantWorker(QObject):
	ready = Signal()
	reply = Signal(str)
	thinking = Signal(str)
	user_message = Signal(str)
	status = Signal(str)
	error = Signal(str)

	def __init__(self, model_name: str) -> None:
		super().__init__()
		self.model_name = model_name
		self.llm = None
		self.stt = None
		self.tts = None
		self._stop_event = threading.Event()

	@Slot()
	def initialize(self) -> None:
		try:
			logger.info("Initializing assistant services with model %s", self.model_name)
			self.status.emit("Loading assistant...")
			self.stt = STT(AppConfig().stt)
			self.llm = LocalLLM(
				model=self.model_name,
				system_prompt=(
					"You are a local voice assistant named Anna. "
					"Give short, natural answers suitable for speech."
				),
			)
			self.tts = PiperTTS(model_path=PIPER_MODEL, audio_device=AUDIO_DEVICE)
			self.status.emit("Ready")
			self.ready.emit()
		except Exception as exc:
			logger.exception("Failed to initialize assistant services")
			self.error.emit(f"Could not start assistant: {exc}")

	@Slot(str)
	def ask(self, text: str) -> None:
		if self.llm and text.strip():
			logger.info("Processing text request")
			self._ask(text.strip())

	@Slot()
	def listen(self) -> None:
		if not self.stt:
			return
		try:
			logger.info("Starting voice request")
			self.status.emit("Listening...")
			text = self.stt.listen().strip()
			if text:
				self._ask(text)
			else:
				self.status.emit("I did not hear anything")
		except Exception as exc:
			logger.exception("Voice request failed")
			self.error.emit(f"Voice input failed: {exc}")
		finally:
			if self.llm:
				self.status.emit("Ready")

	def _ask(self, text: str) -> None:
		llm = self.llm
		tts = self.tts
		if llm is None or tts is None:
			return

		try:
			logger.info("Processing assistant request")
			self.user_message.emit(text)
			self.status.emit("Thinking...")
			response = llm.ask(text)
			if llm.thinking:
				self.thinking.emit(llm.thinking)
			if response:
				self.reply.emit(response)
				self.status.emit("Speaking...")
				tts.speak(response)
				while tts.is_playing():
					if self._stop_event.wait(0.05):
						break
				self._stop_event.clear()
			self.status.emit("Ready")
		except Exception as exc:
			logger.exception("Assistant request failed")
			self.error.emit(f"Assistant failed: {exc}")
			self.status.emit("Ready")

	def stop_speech(self) -> None:
		logger.info("Stopping assistant speech")
		self._stop_event.set()
		if self.tts:
			self.tts.stop()

	def close(self) -> None:
		logger.info("Closing assistant worker")
		self.stop_speech()
		if self.stt:
			self.stt.recorder.microphone.stop_recording()