from PySide6.QtWidgets import QDialog, QListWidget, QListWidgetItem, QPushButton, QVBoxLayout


class HistoryDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Chat History")
        self.resize(500, 420)

        layout = QVBoxLayout(self)
        self.list_widget = QListWidget()
        self.list_widget.setWordWrap(True)
        layout.addWidget(self.list_widget)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

    def populate(self, rows) -> None:
        self.list_widget.clear()

        if not rows:
            self.list_widget.addItem(QListWidgetItem("No chat history yet."))
            return

        for prompt, reply, _, timestamp in rows:
            entry = (
                f"{timestamp}\n"
                f"You: {prompt}\n"
                f"Anna: {reply}"
            )
            self.list_widget.addItem(QListWidgetItem(entry))
