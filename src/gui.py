import logging
import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication


logger = logging.getLogger(__name__)

from gui.chat_window import ChatWindow


def main() -> None:
	logging.basicConfig(
		level=logging.INFO,
		format="%(asctime)s %(levelname)s %(name)s: %(message)s",
	)
	logger.info("Starting Anna GUI")
	app = QApplication(sys.argv)
	window = ChatWindow()
	window.show()
	result = app.exec()
	logger.info("Anna GUI stopped with exit code %d", result)
	sys.exit(result)


if __name__ == "__main__":
	main()