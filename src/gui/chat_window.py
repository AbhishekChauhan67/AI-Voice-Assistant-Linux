import logging
from pathlib import Path

from PySide6.QtCore import QThread, Signal, Slot
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
	QHBoxLayout,
	QLabel,
	QLineEdit,
	QListWidget,
	QListWidgetItem,
	QMainWindow,
	QPushButton,
	QVBoxLayout,
	QWidget,
)

try:
	from core.db import ChatHistory
except ModuleNotFoundError:
	from src.core.db import ChatHistory

from .gui_worker import AssistantWorker
from .history_dialog import HistoryDialog
from .styles import CHAT_WINDOW_STYLESHEET


logger = logging.getLogger(__name__)


class ChatWindow(QMainWindow):
	text_requested = Signal(str)
	voice_requested = Signal()

	def __init__(self) -> None:
		super().__init__()
		logger.info("Creating chat window")
		self.setWindowTitle("Anna | Local Assistant")
		self.resize(760, 620)
		self.setMinimumSize(520, 420)

		self.history_db = ChatHistory(str(Path(__file__).resolve().parents[2] / "history.db"))
		self.history_dialog = None
		self.history_view = None

		self.worker_thread = QThread(self)
		self.worker = AssistantWorker(model_name="qwen3:1.7b")
		self.worker.moveToThread(self.worker_thread)
		self.worker_thread.started.connect(self.worker.initialize)
		self.text_requested.connect(self.worker.ask)
		self.voice_requested.connect(self.worker.listen)
		self.worker.ready.connect(self._assistant_ready)
		self.worker.user_message.connect(self._add_user_message)
		self.worker.reply.connect(self._add_assistant_message)
		self.worker.status.connect(self._handle_status)
		self.worker.error.connect(self._show_error)

		self._build_ui()
		self.worker_thread.start()

	def _build_ui(self) -> None:
		self.setStyleSheet(CHAT_WINDOW_STYLESHEET)

		central = QWidget()
		layout = QVBoxLayout(central)
		layout.setContentsMargins(28, 24, 28, 24)
		layout.setSpacing(14)

		header = QHBoxLayout()
		self.quit_button = QPushButton("×")
		self.quit_button.setObjectName("close")
		self.quit_button.setToolTip("Close Anna")
		self.quit_button.clicked.connect(self.close)
		title = QLabel("Anna")
		title.setObjectName("title")
		self.status_label = QLabel("Starting...")
		self.status_label.setObjectName("status")
		self.history_button = QPushButton("History")
		self.history_button.setObjectName("history")
		self.history_button.clicked.connect(self._show_history)
		header.addWidget(self.quit_button)
		header.addWidget(title)
		header.addStretch()
		header.addWidget(self.history_button)
		header.addWidget(self.status_label)
		layout.addLayout(header)

		self.messages = QListWidget()
		self.messages.setWordWrap(True)
		self.messages.setFont(QFont("Sans Serif", 11))
		layout.addWidget(self.messages, 1)

		controls = QHBoxLayout()
		self.input = QLineEdit()
		self.input.setPlaceholderText("Type a message...")
		self.input.returnPressed.connect(self._send_text)
		self.send_button = QPushButton("Send")
		self.send_button.setObjectName("send")
		self.send_button.clicked.connect(self._send_text)
		self.voice_button = QPushButton("Voice")
		self.voice_button.setObjectName("voice")
		self.voice_button.clicked.connect(self._listen_for_voice)
		self.stop_button = QPushButton("Stop")
		self.stop_button.setObjectName("stop")
		self.stop_button.setToolTip("Stop Anna speaking")
		self.stop_button.setVisible(False)
		self.stop_button.clicked.connect(self._stop_speech)
		controls.addWidget(self.input, 1)
		controls.addWidget(self.voice_button)
		controls.addWidget(self.stop_button)
		controls.addWidget(self.send_button)
		layout.addLayout(controls)

		self.setCentralWidget(central)
		self._set_controls_enabled(False)

	@Slot()
	def _assistant_ready(self) -> None:
		logger.info("Assistant is ready for input")
		self._set_controls_enabled(True)
		self._add_assistant_message("Hello. I am Anna. How can I help?")

	@Slot(str)
	def _add_user_message(self, text: str) -> None:
		self._add_message(f"You: {text}")

	@Slot(str)
	def _add_assistant_message(self, text: str) -> None:
		self._add_message(f"Anna: {text}")

	def _add_message(self, text: str) -> None:
		self.messages.addItem(QListWidgetItem(text))
		self.messages.scrollToBottom()

	@Slot(str)
	def _set_status(self, text: str) -> None:
		self.status_label.setText(text)

	@Slot(str)
	def _handle_status(self, text: str) -> None:
		logger.debug("Assistant status changed: %s", text)
		self._set_status(text)
		self.stop_button.setVisible(text == "Speaking...")
		self.stop_button.setEnabled(text == "Speaking...")
		if text == "Ready":
			self._set_controls_enabled(True)

	@Slot(str)
	def _show_error(self, message: str) -> None:
		logger.error("Displaying assistant error: %s", message)
		self._set_status("Error")
		self.stop_button.setVisible(False)
		self.stop_button.setEnabled(False)
		self._add_message(message)

	def _show_history(self) -> None:
		if self.history_dialog is None:
			self.history_dialog = HistoryDialog(self)

		history_rows = self.history_db.get_recent(20)
		self.history_dialog.populate(history_rows)
		self.history_dialog.show()
		self.history_dialog.raise_()
		self.history_dialog.activateWindow()

	def _send_text(self) -> None:
		text = self.input.text().strip()
		if not text:
			return
		logger.info("Sending text message: %s", text)
		self.input.clear()
		self._set_controls_enabled(False)
		self.text_requested.emit(text)

	def _listen_for_voice(self) -> None:
		logger.info("Starting voice input from GUI")
		self._set_controls_enabled(False)
		self.voice_requested.emit()

	def _stop_speech(self) -> None:
		logger.info("Stopping Anna speech from GUI")
		self.worker.stop_speech()

	def _set_controls_enabled(self, enabled: bool) -> None:
		self.input.setEnabled(enabled)
		self.send_button.setEnabled(enabled)
		self.voice_button.setEnabled(enabled)
		if not enabled:
			self.stop_button.setEnabled(False)

	def closeEvent(self, event) -> None:
		logger.info("Closing chat window")
		self.worker.close()
		self.worker_thread.quit()
		self.worker_thread.wait()
		event.accept()