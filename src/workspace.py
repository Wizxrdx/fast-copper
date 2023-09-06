import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout


class workspace(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.current_image_index = 0
        self.image_label = None
        self.image_paths = []

        self.initUI()

    def initUI(self):
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.showImage(self.current_image_index)

        next_button = QPushButton('Next', self)
        next_button.clicked.connect(self.showNextImage)

        prev_button = QPushButton('Previous', self)
        prev_button.clicked.connect(self.showPreviousImage)

        button_layout = QHBoxLayout()
        button_layout.addWidget(prev_button)
        button_layout.addWidget(next_button)

        gallery_layout = QVBoxLayout()
        gallery_layout.addWidget(self.image_label)
        gallery_layout.addLayout(button_layout)

        self.setLayout(gallery_layout)
        
    def loadImages(self, images_path):
        self.image_paths = images_path
        self.current_image_index = 0

    def showImage(self, index):
        if 0 <= index < len(self.image_paths):
            image_path = self.image_paths[index]
            pixmap = QPixmap(image_path)
            self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio))

    def showNextImage(self):
        self.current_image_index += 1
        if self.current_image_index >= len(self.image_paths):
            self.current_image_index = 0
        self.showImage(self.current_image_index)

    def showPreviousImage(self):
        self.current_image_index -= 1
        if self.current_image_index < 0:
            self.current_image_index = len(self.image_paths) - 1
        self.showImage(self.current_image_index)
