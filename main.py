import sys
from PySide6.QtWidgets import QApplication
from db.database import init_db


def main():
    app = QApplication(sys.argv)

    from ui.main_window import MainWindow

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    init_db()
    main()

