import maya.cmds as cmds
import maya.OpenMaya as om
from PySide2.QtWidgets import QMainWindow, QApplication, QVBoxLayout

class CameraShake(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Camera Shake")

        self.create_ui()

    def create_ui(self):
        layout = QVBoxLayout()

        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication.instance()
    if not app:
        app = QApplication()
    
    # Create and show the UI window
    window = CameraShake()
    window.show()