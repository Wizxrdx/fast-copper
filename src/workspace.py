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
        
        self.showImage(self.current_image_index)

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



To add a box that moves along with the cursor in your image gallery, you can use a custom widget and override the mouseMoveEvent method to update the box's position. Here's an updated example:

python
Copy code
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QScrollArea, QPushButton, QHBoxLayout
from PyQt5.QtGui import QPixmap, QImage, QPainter, QColor, QCursor, QMouseEvent
from PyQt5.QtCore import Qt, QPoint

class ImageGallery(QWidget):
    def __init__(self, image_paths):
        super().__init__()
        self.image_paths = image_paths
        self.current_image_index = 0

        self.initUI()

    def initUI(self):
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.showImage(self.current_image_index)

        next_button = QPushButton('Next', self)
        next_button.clicked.connect(self.showNextImage)

        prev_button = QPushButton('Previous', self)
        prev_button.clicked.connect(self.showPreviousImage)

        extract_button = QPushButton('Extract', self)
        extract_button.clicked.connect(self.extractImage)

        button_layout = QHBoxLayout()
        button_layout.addWidget(prev_button)
        button_layout.addWidget(next_button)
        button_layout.addWidget(extract_button)

        gallery_layout = QVBoxLayout()
        gallery_layout.addWidget(self.image_label)
        gallery_layout.addLayout(button_layout)

        self.setLayout(gallery_layout)

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
        
    def extractImage(self):
        if 0 <= self.current_image_index < len(self.image_paths):
            image_path = self.image_paths[self.current_image_index]
            QMessageBox.information(self, "Image Extraction", f"Image path: {image_path}")

class MouseBox(QWidget):
    def __init__(self):
        super().__init__()
        self.setCursor(Qt.BlankCursor)
        self.setGeometry(0, 0, 50, 50)  # Set the initial size and position of the box
        self.box_color = QColor(255, 0, 0, 100)  # Red color for the box

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), self.box_color)

    def updateBoxPosition(self, event):
        # Update the box's position to follow the cursor
        cursor_pos = event.pos()
        self.move(cursor_pos - QPoint(self.width() // 2, self.height() // 2))
        self.update()
        
        def updateBoxSize(self, delta):
            current_size = self.size()
            new_size = current_size + delta
            if new_size.width() >= 10 and new_size.height() >= 10:  # Minimum size constraint
                self.setFixedSize(new_size)
                self.update()

    def mouseMoveEvent(self, event: QMouseEvent):
        self.updateBoxPosition(event)
        
    def wheelEvent(self, event):
    	delta = event.angleDelta().y() // 120
        if delta != 0:
            self.updateBoxSize(QSize(delta, delta))