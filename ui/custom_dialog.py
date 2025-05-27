from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QLabel


class CustomDialog(QtWidgets.QDialog):
    def __init__(self, text, title="Ошибка!", parent=None):
        super().__init__(parent)

        self.setWindowTitle(title)

        QBtn = (QtWidgets.QDialogButtonBox.StandardButton.Ok)

        self.buttonBox = QtWidgets.QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        layout = QVBoxLayout()
        message = QLabel(text)
        layout.addWidget(message, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.buttonBox, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)
        self.adjustSize()
