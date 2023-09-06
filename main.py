import sys

from PyQt5.QtWidgets import QApplication, QStackedWidget

from src.manager import manager
from src.workspace import workspace


class MainApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 400, 200)
        self.setWindowTitle('FastCropper')

        self.addWidget(manager(self))
        self.addWidget(workspace(self))

    def sendImages(self, images):
        self.setCurrentIndex(1)
        self.currentWidget().loadImages(images)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    sys.excepthook = except_hook

app = QApplication(sys.argv)
win = MainApp()
win.show()

sys.exit(app.exec_())
