import os
import sys
import base64
import urllib.parse
from pathlib import Path
from PyQt5 import QtWidgets, QtGui, QtCore

# Base64-encoded icon (replace this with your actual Base64 string)
icon_base64 = '''
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
'''

def get_folder_size(folder):
    """Returns the size of the folder in bytes."""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):  # Only count the size if the file exists
                total_size += os.path.getsize(fp)
    return total_size

def find_largest_folders(drive, top_n=10):
    """Finds the largest folders in the specified directory."""
    folder_sizes = []
    
    for folder in Path(drive).iterdir():
        if folder.is_dir():
            try:
                folder_size = get_folder_size(folder)
                folder_sizes.append((folder, folder_size))
            except PermissionError:
                pass
    
    folder_sizes.sort(key=lambda x: x[1], reverse=True)
    
    return folder_sizes[:top_n]

class Worker(QtCore.QThread):
    result_ready = QtCore.pyqtSignal(list)  # Signal to communicate when the result is ready
    def __init__(self, folder):
        super().__init__()
        self.folder = folder
    
    def run(self):
        # Analyze the largest folders in the specified directory
        largest_folders = find_largest_folders(self.folder, top_n=10)
        self.result_ready.emit(largest_folders)  # Emit the result

class DriveAnalyzerApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Drive Analyzer')
        self.setGeometry(300, 300, 600, 400)

        # Set window icon using Base64
        icon_data = base64.b64decode(icon_base64)
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(icon_data)
        icon = QtGui.QIcon(pixmap)
        self.setWindowIcon(icon)

        # Create layout
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        # Create a label for the drive input
        drive_label = QtWidgets.QLabel("Enter Drive (e.g., C:\\):", self)
        layout.addWidget(drive_label)

        # Create a line edit for the user to input the drive
        self.drive_input = QtWidgets.QLineEdit(self)
        self.drive_input.setPlaceholderText("Enter drive letter (e.g., C:\\)")
        layout.addWidget(self.drive_input)

        # Create a button to start the scan
        self.scan_button = QtWidgets.QPushButton("Analyze Drive", self)
        self.scan_button.clicked.connect(self.start_analysis)
        self.scan_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        layout.addWidget(self.scan_button)

        # Create a text area to display the results and make it interactive
        self.result_area = QtWidgets.QTextBrowser(self)
        self.result_area.setReadOnly(True)
        self.result_area.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse | QtCore.Qt.LinksAccessibleByMouse)
        self.result_area.setStyleSheet("background-color: #f2f2f2; border: 1px solid #ccc; padding: 10px;")
        self.result_area.anchorClicked.connect(self.analyze_folder)  # Handle anchor clicks
        layout.addWidget(self.result_area)

        # Set the layout
        self.setLayout(layout)

    def start_analysis(self):
        """Start analyzing the drive or folder."""
        folder = self.drive_input.text().strip()  # Get the drive from the input field
        if not folder or not isinstance(folder, str):  # Ensure it's a valid folder path
            folder = "C:\\"  # Default to C: if input is invalid
        
        self.result_area.append(f"Analyzing {folder} ...")
        self.worker = Worker(folder)  # Pass the folder path to the worker
        self.worker.result_ready.connect(self.display_results)
        self.worker.start()

    def display_results(self, largest_folders):
        self.result_area.clear()  # Clear previous results
        self.result_area.append("Top largest folders:\n")
        for folder, size in largest_folders:
            folder_info = f"<a href='{folder}'>{folder}</a>: {size / (1024 * 1024):.2f} MB"
            self.result_area.append(folder_info)

    def analyze_folder(self, url):
        folder_path = url.toString()  # Get the URL string
        if folder_path.startswith("file:///"):
            folder_path = folder_path.replace("file:///", "", 1)  # Remove file:/// prefix

        # Decode any URL-encoded characters
        folder_path = urllib.parse.unquote(folder_path)  # Decode the URL
        folder_path = folder_path.replace('/', '\\')  # Correct path format for Windows

        # Ensure folder_path is a valid path and exists
        if folder_path and Path(folder_path).exists():
            self.start_analysis(folder_path)
        else:
            QtWidgets.QMessageBox.warning(self, "Invalid Path", "The selected folder does not exist or is invalid.")

# Main entry point
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    analyzer = DriveAnalyzerApp()
    analyzer.show()
    sys.exit(app.exec_())
