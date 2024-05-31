import sys
from PyQt6 import QtCore, QtGui, QtWidgets
import requests


class FileDataViewer(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QR Segregation App")
        self.setGeometry(100, 100, 800, 450)

        main_widget = QtWidgets.QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QtWidgets.QHBoxLayout(main_widget)

        # Left layout for file upload
        left_layout = QtWidgets.QVBoxLayout()

        # File selection frame
        file_frame = QtWidgets.QGroupBox("Image Upload")
        file_layout = QtWidgets.QVBoxLayout(file_frame)
        file_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        # Upload Images button
        upload_images_button = QtWidgets.QPushButton("Upload Images")
        upload_images_button.clicked.connect(self.upload_images)
        upload_images_button.setFixedSize(120, 30)  # Set fixed size
        upload_images_button.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)  # Set size policy
        file_layout.addWidget(upload_images_button)

        # Send Images button
        send_images_button = QtWidgets.QPushButton("Send Images")
        send_images_button.clicked.connect(self.send_images)
        send_images_button.setFixedSize(120, 30)  # Set fixed size
        send_images_button.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)  # Set size policy
        file_layout.addWidget(send_images_button)

        left_layout.addWidget(file_frame)

        # Right layout for image display
        right_layout = QtWidgets.QVBoxLayout()

        # Image display area
        self.image_scroll_area = QtWidgets.QScrollArea()
        self.image_scroll_area.setWidgetResizable(True)
        self.image_scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.image_scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        right_layout.addWidget(self.image_scroll_area)

        self.image_container = QtWidgets.QWidget()
        self.image_layout = QtWidgets.QVBoxLayout(self.image_container)
        self.image_scroll_area.setWidget(self.image_container)

        main_layout.addLayout(left_layout, 1)  # Set stretch factor to 1
        main_layout.addLayout(right_layout, 1)  # Set stretch factor to 1

    def upload_images(self):
        file_dialog = QtWidgets.QFileDialog()
        file_paths, _ = file_dialog.getOpenFileNames(self, "Upload Images", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if file_paths:
            print("Selected image paths:", file_paths)
            for file_path in file_paths:
                image_label = QtWidgets.QLabel()
                pixmap = QtGui.QPixmap(file_path)
                image_label.setPixmap(pixmap)
                self.image_layout.addWidget(image_label)

    def send_images(self):
        # Construct the request body with image data
        files = []
        for i in range(self.image_layout.count()):
            widget = self.image_layout.itemAt(i).widget()
            if isinstance(widget, QtWidgets.QLabel):
                pixmap = widget.pixmap()
                image_path = f"image{i}.jpg"
                pixmap.save(image_path, "JPEG")  # Save images locally for testing
                files.append(("images", (image_path, open(image_path, "rb"), "image/jpeg")))
        
        # Define the API endpoint to send the images
        api_endpoint = "http://192.168.51.17:5000/post"  # Replace with the actual API endpoint

        # Send the request to the API endpoint
        try:
            response = requests.post(api_endpoint, files=files)
            response.raise_for_status()  # Check for HTTP errors
            print("Images sent successfully.")
        except requests.exceptions.RequestException as e:
            print("Error:", e)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = FileDataViewer()
    window.show()
    sys.exit(app.exec())