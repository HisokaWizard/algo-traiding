import sys

from PyQt6.QtWidgets import QApplication

from src.ui.general_window import GeneralWindow


def main():
    # sandbox()
    app = QApplication(sys.argv)
    window = GeneralWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
