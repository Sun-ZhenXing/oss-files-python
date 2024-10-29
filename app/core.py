import sys

from PySide6.QtCore import QTranslator
from PySide6.QtWidgets import QApplication

from app.widgets.main import MainWidget


def main():
    translator = QTranslator()
    translator.load("./resources/i18n/qt_zh_CN.qm")
    app = QApplication(sys.argv)
    app.installTranslator(translator)

    window = MainWidget()
    window.show()
    sys.exit(app.exec())
