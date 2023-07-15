# Image processing App

This application allows the user to perform basic image processing operations on an image file. The user can open an image file, apply various processing operations, and save the processed image to a new file.

# Installation

To install the required packages, run the following command:

```Text Python
pip install opencv-python PyQt5
```

# Code explination

- Importing Libraries  
  The first step in the code is to import the necessary libraries. In this case, we need cv2 from the OpenCV library for loading and saving images, QApplication, QMainWindow, QLabel, QPixmap, QVBoxLayout, QHBoxLayout, QFileDialog, QDialog, QSpinBox, and QPushButton from the PyQt5 library for creating the GUI, and sys for exiting the application.

```Text python
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QFileDialog, QDialog, QSpinBox, QPushButton
import sys
```

- Resize Dialog  
  The ResizeDialog class is a QDialog that is used to prompt the user for a new size when resizing an image. It contains two QSpinBox widgets for the width and height inputs, an "OK" button, and a "Cancel" button. When the user clicks the "OK" button, the get_size method is called, which returns the selected size as a tuple of (width, height).

```Text python
class ResizeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Resize Image")
        self.width_spinbox = QSpinBox()
        self.width_spinbox.setRange(1, 10000)
        self.height_spinbox = QSpinBox()
        self.height_spinbox.setRange(1, 10000)
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Width:"))
        layout.addWidget(self.width_spinbox)
        layout.addWidget(QLabel("Height:"))
        layout.addWidget(self.height_spinbox)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def get_size(self):
        return (self.width_spinbox.value(), self.height_spinbox.value())
```

- Image Processing UI  
  The ImageProcessingUI class is a QMainWindow that represents the main window of the application. It contains several widgets and layouts for displaying the image and the processing buttons.

```Text python
class ImageProcessingUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Processing")
        self.setFixedSize(800, 600)
        self.create_menu_bar()
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout()
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label)
        self.create_processing_buttons()
        self.main_widget.setLayout(self.layout)
        self.processed_image = None
        self.steps = []

    def create_menu_bar(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        open_action = file_menu.addAction("Open")
        open_action.triggered.connect(self.open_image)

    def create_processing_buttons(self):
        button_layout = QHBoxLayout()
        upload_button = QPushButton("Upload Image")
        upload_button.clicked.connect(self.open_image)
        button_layout.addWidget(upload_button)
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
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_image)
        button_layout.addWidget(save_button)
        undo_button = QPushButton("Undo")
        undo_button.clicked.connect(self.undo_step)
        button_layout.addWidget(undo_button)
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear_all)
        button_layout.addWidget(clear_button)
        self.layout.addLayout(button_layout)
```

When the application is launched, the **init** method of the ImageProcessingUI class is called. This method sets the title of the main window and sets a fixed size for the window. It then creates the menu bar and adds a "File" menu with an "Open" action for opening an image file.

```
def __init__(self):
    super().__init__()
    self.setWindowTitle("Image Processing")
    self.setFixedSize(800, 600)
    self.create_menu_bar()
```

The open_image method is called when the user clicks the "Upload Image" button or the "Open" action in the menu bar. It opens a file dialog and prompts the user to select an image file. If a file is selected, the image is loaded using the OpenCV library and displayed in the image label. The processed image is set to the loaded image, and the steps list is initialized with the loaded image as the first step.

```
def open_image(self):
    file_dialog = QFileDialog()
    file_dialog.setNameFilter("Images (*.jpg *.png *.bmp)")
    if file_dialog.exec_() == QDialog.Accepted:
        filename = file_dialog.selectedFiles()[0]
        image = cv2.imread(filename)
        self.processed_image = image
        self.steps = [image]
        self.show_image(image)
```

The show_image method is called to display the loaded image in the image label. It converts the image to RGB format and creates a QImage and QPixmap object for displaying the image.

```
def show_image(self, image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    qimage = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
    pixmap = QPixmap.fromImage(qimage)
    self.image_label.setPixmap(pixmap)
```

The remaining methods (apply_gray, apply_blur, apply_rotate, apply_resize, apply_edge_detection, save_image, undo_step, and clear_all) are called when the user clicks the corresponding processing button. These methods perform the desired operation on the image, add the new image to the steps list, and display the processed image in the image label.

```
def apply_gray(self):
    image = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2GRAY)
    self.processed_image = image
    self.steps.append(image)
    self.show_image(image)

def apply_blur(self):
    image = cv2.GaussianBlur(self.processed_image, (5, 5), 0)
    self.processed_image = image
    self.steps.append(image)
    self.show_image(image)

def apply_rotate(self):
    image = cv2.rotate(self.processed_image, cv2.ROTATE_90_CLOCKWISE)
    self.processed_image = image
    self.steps.append(image)
    self.show_image(image)

def apply_resize(self):
    resize_dialog = ResizeDialog(self)
    if resize_dialog.exec_() == QDialog.Accepted:
        size = resize_dialog.get_size()
        image = cv2.resize(self.processed_image, size)
        self.processed_image = image
        self.steps.append(image)
        self.show_image(image)

def apply_edge_detection(self):
    gray = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    color_edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    image = cv2.bitwise_and(self.processed_image, color_edges)
    self.processed_image = image
    self.steps.append(image)
    self.show_image(image)

def save_image(self):
    file_dialog = QFileDialog()
    file_dialog.setNameFilter("Images (*.jpg *.png *.bmp)")
    if file_dialog.exec_() == QDialog.Accepted:
        filename = file_dialog.selectedFiles()[0]
        cv2.imwrite(filename, self.processed_image)

def undo_step(self):
    if len(self.steps) > 1:
        self.steps.pop()
        image = self.steps[-1]
        self.processed_image = image
        self.show_image(image)

def clear_all(self):
    self.processed_image = self.steps[0]
    self.steps = [self.steps[0]]
    self.show_image(self.processed_image)
```

The save_image method is called when the user clicks the "Save" button. It opens a file dialog and prompts the user to select a location and format for saving the processed image. If a location is selected, the processed image is saved using the OpenCV library.

The undo_step method is called when the user clicks the "Undo" button. It removes the most recent step from the steps list and displays the previous version of the image in the image label.

The clear_all method is called when the user clicks the "Clear" button. It resets the processed image to the original image and clears the steps list.

At the end of the code, there is a main block that creates an instance of the ImageProcessingUI class and calls the show method to display the main window. The sys.exit method is used to exit the application when the user closes the window.

```
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageProcessingUI()
    window.show()
    sys.exit(app.exec_())
```

# Usage

To run the application, execute the following command:

```Text python
python image_processing_app.py
```

This will launch the main window of the application. From here, the user can open an image file, apply various processing operations, and save the processed image to a new file.

# Opening an Image

To open an image file, click the "Upload Image" button or select the "Open" option from the "File" menu. This will open a file dialog where the user can select an image file. Once an image file is selected, it will be displayed in the main window.

# Processing Operations

The following processing operations are available:

```
Grayscale: Converts the image to grayscale.
Blur: Applies a Gaussian blur to the image.
Rotate: Rotates the image 90 degrees clockwise.
Resize: Prompts the user for a new size and resizes the image.
Edge Detection: Applies Canny edge detection to the image.
Undo: Undoes the most recent processing operation.
Clear: Clears all processing operations and resets the image to its original state.
```

To apply a processing operation, click the corresponding button. The processed image will be displayed in the main window. To undo the most recent processing operation, click the "Undo" button. To clear all processing operations and reset the image to its original state, click the "Clear" button.

# Saving the Processed Image

To save the processed image to a new file, click the "Save" button. This will open a file dialog where the user can select a location and format for the new file.
