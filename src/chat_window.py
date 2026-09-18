import logging

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
	from gui_worker import AssistantWorker
except ModuleNotFoundError:
	from src.gui_worker import AssistantWorker


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

		self.worker_thread = QThread(self)
		self.worker = AssistantWorker(model_name="qwen3:4b")
		self.worker.moveToThread(self.worker_thread)
		self.worker_thread.started.connect(self.worker.initialize)
		self.text_requested.connect(self.worker.ask)
		self.voice_requested.connect(self.worker.listen)
		self.worker.ready.connect(self._assistant_ready)
		self.worker.user_message.connect(self._add_user_message)
		self.worker.thinking.connect(self._add_thinking)
		self.worker.reply.connect(self._add_assistant_message)
		self.worker.status.connect(self._handle_status)
		self.worker.error.connect(self._show_error)

		self._build_ui()
		self.worker_thread.start()

	def _build_ui(self) -> None:
		self.setStyleSheet(
			"""
			QMainWindow { background: #f5f7fb; }
			QLabel#title { color: #172033; font-size: 22px; font-weight: 700; }
			QLabel#status { color: #647089; font-size: 13px; }
			QListWidget { background: #ffffff; border: 1px solid #dce2ed; border-radius: 12px; padding: 12px; }
			QListWidget::item { padding: 10px; color: #202a3d; }
			QLineEdit { background: #ffffff; border: 1px solid #cbd4e3; border-radius: 10px; padding: 12px; font-size: 14px; }
			QPushButton { border: 0; border-radius: 10px; padding: 11px 16px; font-weight: 600; }
			QPushButton#send { background: #3264d6; color: white; }
			QPushButton#voice { background: #e6edff; color: #244da9; }
			QPushButton#stop { background: #ffe8e6; color: #b4332d; }
			QPushButton:disabled { background: #e4e8ef; color: #8b94a5; }
			"""
		)

		central = QWidget()
		layout = QVBoxLayout(central)
		layout.setContentsMargins(28, 24, 28, 24)
		layout.setSpacing(14)

		header = QHBoxLayout()
		title = QLabel("Anna")
		title.setObjectName("title")
		self.status_label = QLabel("Starting...")
		self.status_label.setObjectName("status")
		header.addWidget(title)
		header.addStretch()
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
		self.stop_button.clicked.connect(self.worker.stop_speech)
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

	@Slot(str)
	def _add_thinking(self, text: str) -> None:
		self._add_message(f"Anna thinking: {text}")

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