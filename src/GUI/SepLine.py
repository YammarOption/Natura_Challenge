from PyQt5.QtWidgets import QFrame

class SepLine(QFrame):
    """
    A simple separator line
    """
    def __init__(self, width=3,style="solid",parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)
        self.setStyleSheet(f"border: {width}px {style} white;")