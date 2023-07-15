import cv2
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QMenuBar, QMenu, QAction, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, \
    QLabel, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLabel, QSpinBox, QDialogButtonBox, QVBoxLayout, QHBoxLayout

class ResizeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Resize Image")

        # Create the size input widgets
        width_label = QLabel("Width:")
        self.width_spinbox = QSpinBox()
        self.width_spinbox.setRange(1, 10000)
        height_label = QLabel("Height:")
        self.height_spinbox = QSpinBox()
        self.height_spinbox.setRange(1, 10000)

        # Create the OK and Cancel buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        # Create the main layout and add the widgets
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        size_layout = QHBoxLayout()
        size_layout.addWidget(width_label)
        size_layout.addWidget(self.width_spinbox)
        size_layout.addWidget(height_label)
        size_layout.addWidget(self.height_spinbox)
        main_layout.addLayout(size_layout)
        main_layout.addWidget(button_box)

    def get_size(self):
        # Return the selected size as a tuple of (width, height)
        return (self.width_spinbox.value(), self.height_spinbox.value())


class ImageProcessingUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Processing")
        self.setFixedSize(1050, 600)  # set a fixed size for the main window
        self.image = None
        self.processed_image = None
        self.steps = []
        self.current_step = -1

        # Create the menu bar
        menubar = QMenuBar()
        file_menu = QMenu("File")
        menubar.addMenu(file_menu)
        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_image)
        file_menu.addAction(open_action)
        self.setMenuBar(menubar)

        # Create the main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        # Create the image upload button
        upload_button = QPushButton("Upload Image")
        upload_button.clicked.connect(self.open_image)
        main_layout.addWidget(upload_button)

        # Create the image display label
        self.image_label = QLabel()
        self.image_label.setFixedSize(1000,550)
        self.image_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.image_label)

        # Create the image processing buttons
        button_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)
        gray_button = QPushButton("Grayscale")
        gray_button.clicked.connect(self.apply_gray)
        button_layout.addWidget(gray_button)
        blur_button = QPushButton("Blur")
        blur_button.clicked.connect(self.apply_blur)
        button_layout.addWidget(blur_button)
        rotate_button = QPushButton("Rotate")
        rotate_button.clicked.connect(self.apply_rotate)
        button_layout.addWidget(rotate_button)
        resize_button = QPushButton("Resize")
        resize_button.clicked.connect(self.apply_resize)
        button_layout.addWidget(resize_button)
        edge_detection_button = QPushButton("Edge Detection")
        edge_detection_button.clicked.connect(self.apply_edge_detection)
        button_layout.addWidget(edge_detection_button)

        # Create the save button
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_image)
        button_layout.addWidget(save_button)

        # Create the undo and clear buttons
        undo_button = QPushButton("Undo")
        undo_button.clicked.connect(self.undo_step)
        button_layout.addWidget(undo_button)
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear_all)
        button_layout.addWidget(clear_button)

        # Add a stretch to the bottom of the layout to fill any remaining space
        main_layout.addStretch()

        # Set the main widget as the central widget
        self.setCentralWidget(main_widget)

    def open_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.jpg *.png *.bmp)")
        if file_path:
            # Load the image and display it
            self.image = cv2.imread(file_path)
            self.processed_image = self.image.copy()
            self.steps = [self.image.copy()]
            self.current_step = 0
            self.show_image(self.processed_image)

    def show_image(self, image):
        # Convert the image to RGB and display it
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap(q_image)
        self.image_label.setPixmap(pixmap)

    def apply_gray(self):
        if self.processed_image is not None:
            # Apply the grayscale step and add it to the steps list
            if len(self.processed_image.shape) == 2:
                gray = self.processed_image
            else:
                gray = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2GRAY)
            self.steps.append(gray)
            self.current_step += 1
            self.processed_image = gray
            self.show_image(self.processed_image)

    def apply_blur(self):
        if self.processed_image is not None:
            # Apply the blur step and add it to the steps list
            blur = cv2.GaussianBlur(self.processed_image, (5, 5), 0)
            self.steps.append(blur)
            self.current_step += 1
            self.processed_image = blur
            self.show_image(self.processed_image)

    def apply_rotate(self):
        if self.processed_image is not None:
            # Apply the rotate step and add it to the steps list
            rotated = cv2.rotate(self.processed_image, cv2.ROTATE_90_CLOCKWISE)
            self.steps.append(rotated)
            self.current_step += 1
            self.processed_image = rotated
            self.show_image(self.processed_image)

    def apply_resize(self):
        if self.processed_image is not None:
            # Prompt the user for the new size
            size_dialog = ResizeDialog(self)
            if size_dialog.exec_():
                new_size = size_dialog.get_size()
                if new_size != self.processed_image.shape[:2]:
                    # Apply the resize step and add it to the steps list
                    resized = cv2.resize(self.processed_image, new_size)
                    self.steps.append(resized)
                    self.current_step += 1
                    self.processed_image = resized
                    self.show_image(self.processed_image)

    def apply_edge_detection(self):
        if self.processed_image is not None:
            # Apply the edge detection step and add it to the steps list
            gray = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 200)
            edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            self.steps.append(edges)
            self.current_step += 1
            self.processed_image = edges
            self.show_image(self.processed_image)
    def save_image(self):
        if self.processed_image is not None:
            # Prompt the user for the save location and format
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Image Files (*.jpg *.png *.bmp)")
            if file_path:
                # Save the image
                cv2.imwrite(file_path, self.processed_image)

    def undo_step(self):
        if len(self.steps) > 1 and self.current_step > 0:
            # Remove the current step from the steps list and display the previous step
            self.steps.pop()
            self.current_step -= 1
            self.processed_image = self.steps[self.current_step]
            self.show_image(self.processed_image)

    def clear_all(self):
        # Clear all the processed steps and display the original image
        if self.image is not None:
            self.processed_image = self.image.copy()
            self.steps = [self.image.copy()]
            self.current_step = 0
            self.show_image(self.processed_image)
import sys
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageProcessingUI()
    window.show()
    sys.exit(app.exec_())