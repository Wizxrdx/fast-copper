from PyQt5.QtWidgets import QWidget, QPushButton, QFileDialog


class manager(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.button = None
        self.initUI()

    def initUI(self):
        self.button = QPushButton('Select Images...', self)
        self.button.setGeometry(150, 80, 100, 30)
        self.button.clicked.connect(self.openFileDialog)

    def openFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly  # Open in read-only mode
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("Image Files (*.png *.jpg *.jpeg *.bmp *.gif)")
        file_dialog.setViewMode(QFileDialog.List)

        file_name, _ = file_dialog.getOpenFileNames(self, "Select images to edit", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)

        if file_name:
            self.parent().sendImages(file_name)
