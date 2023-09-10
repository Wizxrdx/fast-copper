import os

from PyQt5.QtCore import Qt, QEvent, QRectF
from PyQt5.QtGui import QPixmap, QWheelEvent, QMouseEvent
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QGraphicsView, QGraphicsScene, \
    QGraphicsRectItem, QGraphicsPixmapItem


class workspace(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.crop_box = None
        self.scene = None
        self.graphics_view = None
        self.active = False
        self.current_image_index = 0
        self.image_paths = []

        self.initUI()

    def initUI(self):
        self.graphics_view = QGraphicsView(self)
        self.graphics_view.setMouseTracking(True)
        self.scene = QGraphicsScene(self)
        self.graphics_view.setScene(self.scene)

        next_button = QPushButton('Next', self)
        next_button.clicked.connect(self.showNextImage)

        prev_button = QPushButton('Previous', self)
        prev_button.clicked.connect(self.showPreviousImage)

        extract_button = QPushButton('Extract', self)
        extract_button.clicked.connect(self.extractImage)

        # Create the crop box as a QGraphicsRectItem
        self.crop_box = QGraphicsRectItem()
        self.crop_box.setRect(0, 0, 100, 100)  # Initial size of the crop box
        self.crop_box.setPen(Qt.green)
        self.crop_box.setFlag(QGraphicsRectItem.ItemIsMovable)
        self.crop_box.setZValue(1)
        self.scene.addItem(self.crop_box)

        # Connect mouse wheel event to adjust the size of the crop box
        self.graphics_view.viewport().installEventFilter(self)

        button_layout = QHBoxLayout()
        button_layout.addWidget(prev_button)
        button_layout.addWidget(next_button)

        gallery_layout = QVBoxLayout()
        gallery_layout.addWidget(self.graphics_view)
        gallery_layout.addLayout(button_layout)
        gallery_layout.addWidget(extract_button)

        self.setLayout(gallery_layout)

    def loadImages(self, images_path):
        self.image_paths = images_path
        self.current_image_index = 0

        self.showImage(self.current_image_index)
        self.active = True

    def showImage(self, index):
        if 0 <= index < len(self.image_paths):
            image_path = self.image_paths[index]
            pixmap = QPixmap(image_path)
            self.graphics_view.setSceneRect(QRectF(pixmap.rect()))
            self.image_item = QGraphicsPixmapItem(pixmap)
            self.scene.addItem(self.image_item)

    def extractImage(self):
        self.parent.extractImages(self.image_paths)

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

    def eventFilter(self, obj, event):
        if obj is self.graphics_view.viewport():
            if event.type() == QEvent.Wheel:
                delta = event.angleDelta().y()  # Get the mouse wheel delta
                if delta > 0:
                    # Increase the size of the crop box
                    self.crop_box.setRect(self.crop_box.rect().x(), self.crop_box.rect().y(),
                                          self.crop_box.rect().width() + 10, self.crop_box.rect().height() + 10)
                elif delta < 0:
                    # Decrease the size of the crop box (with minimum size)
                    if self.crop_box.rect().width() > 20 and self.crop_box.rect().height() > 20:
                        self.crop_box.setRect(self.crop_box.rect().x(), self.crop_box.rect().y(),
                                              self.crop_box.rect().width() - 10, self.crop_box.rect().height() - 10)

            if event.type() == QMouseEvent.MouseMove:
                # Move the crop box to follow the mouse cursor
                mouse_x = event.x()
                mouse_y = event.y()
                crop_width = self.crop_box.rect().width()
                crop_height = self.crop_box.rect().height()
                # self.crop_box.setRect(mouse_x - crop_width / 2, mouse_y - crop_height / 2, crop_width, crop_height)
                self.crop_box.setX(0)
                self.crop_box.setY(0)
                print(mouse_x, mouse_y)

        return super().eventFilter(obj, event)
