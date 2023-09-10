from PyQt5.QtWidgets import QWidget, QPushButton, QFileDialog, QVBoxLayout, QStatusBar, QMainWindow


class manager(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.no_crop_button = None
        self.crop_button = None
        self.initUI()

    def initUI(self):
        self.crop_button = QPushButton('Imitate MNIST Dataset Format Using Raw Images...', self)
        self.crop_button.setDisabled(True)
        self.no_crop_button = QPushButton('Imitate MNIST Dataset Format Using Cropped Images...', self)

        self.crop_button.clicked.connect(self.openFileDialog)
        self.no_crop_button.clicked.connect(lambda: self.openFileDialog(False))

        layout = QVBoxLayout()
        layout.addWidget(self.crop_button)
        layout.addWidget(self.no_crop_button)

        self.setLayout(layout)

    def openFileDialog(self, crop=True):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly  # Open in read-only mode
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("ImageCroppingBox Files (*.png *.jpg *.jpeg *.bmp *.gif)")
        file_dialog.setViewMode(QFileDialog.List)

        file_names, _ = file_dialog.getOpenFileNames(self, "Select images to edit", "", "ImageCroppingBox Files (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)

        if file_names:
            if crop:
                self.parent().sendImages(file_names)
            else:
                self.parent().extractImages(file_names)
