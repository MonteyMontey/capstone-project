import sys
from PyQt5.QtWidgets import QApplication

from gui.app import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    sys._excepthook = sys.excepthook


    def my_exception_hook(exctype, value, traceback):
        """Custom exception hook to print full error traceback"""
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)


    sys.excepthook = my_exception_hook

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
