from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QSizePolicy
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, pyqtSignal

class CounterWidget(QWidget):
    """
    A widget class implementing a counter with a label, a value display, and increment/decrement buttons.
     
    Attributes:
        text (str): The label text for the counter.
        updateScoreSignal (pyqtSignal): A signal emitted when the counter value changes, with the label text and new count as parameters.
        Mainparent (QWidget): The parent widget of this CounterWidget.
        count (int): The current count value of the counter.
        mainlayout (QHBoxLayout): The main layout for the widget, containing the label, buttons, and value display.
        label (QLabel): The label displaying the counter's name.
    """
    
    def __init__(self, parent,updateSignal:pyqtSignal,label_text:str, text_size=12, font_size=12,count=0):
        """
        Class constructor for CounterWidget.

        :param parent: The parent widget of this CounterWidget
        :param label_text: The text to display on the label
        :param text_size: The size of the label text
        :param font_size: The size of the value display font
        :param count: The initial count value
        """
        super().__init__()
        self.text = label_text
        self.updateScoreSignal = updateSignal
        QtGui.QFontDatabase.addApplicationFont("data/Pokemon GB.ttf")
        self.Mainparent= parent
        self.count = count
        self.mainlayout = QHBoxLayout()
        self.mainlayout.setContentsMargins(0, 0, 0, 0)
        if not self.isLevel :self.mainlayout.setSpacing(10)

        self.label = QLabel(label_text)
        self.label.setWordWrap(True)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.value_label = QLabel(str(self.count))
        self.label.setStyleSheet("background-color: black; border:black; color:white")
        self.label.setFont(QtGui.QFont("Sanserif", text_size))

        self.value_label.setStyleSheet("background-color: black; border: black; color:white")
        self.label.setMinimumWidth(50)
        self.value_label.setMinimumWidth(50)
        self.value_label.setAlignment(QtGui.Qt.AlignRight)
        self.label.setAlignment(QtGui.Qt.AlignLeft)
        self.value_label.setFont(QtGui.QFont("Sanserif", font_size))
        
        
        self.mainlayout.addWidget(self.label)
        self.btn_inc = QPushButton('+')
        self.btn_inc.clicked.connect(self.increase)
        self.mainlayout.addWidget(self.btn_inc)
        self.mainlayout.addWidget(self.value_label)

        self.setLayout(self.mainlayout)

    def increase(self):
        self.count += 1
        self.value_label.setText(str(self.count))
        self.updateScoreSignal.emit(self.text, self.count)

    def get_count(self):
        return self.count

    def set_count(self, value):
        self.count = value
        self.value_label.setText(str(self.count))

class LevelCounterWidget(CounterWidget):
    """
    A specialized CounterWidget for tracking levels, without a decrement button and a different layout.
    """
    def __init__(self, parent,updateSignal:pyqtSignal,label_text:str, text_size=12, font_size=12,count=0):
        super().__init__(parent,updateSignal,label_text, text_size, font_size,count)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

class ScoreCounterWidget(CounterWidget):
    """
    A specialized CounterWidget for tracking scores, with a decrement button and a different layout.
    """
    def __init__(self, parent,updateSignal:pyqtSignal,label_text:str, text_size=12, font_size=12,count=0):
        super().__init__(parent,updateSignal,label_text, text_size, font_size,count)
        self.btn_dec = QPushButton('-')
        self.btn_dec.clicked.connect(self.decrease)
        self.mainlayout.addWidget(self.btn_dec)
    
    def decrease(self):
        """
        Decrease the count by 1, ensuring it does not go below 0, and update the display and emit the update signal.
        
        :param self: Descrizione
        """
        self.count = max(0, self.count -1)
        self.value_label.setText(str(self.count))
        self.updateScoreSignal.emit(self.text, self.count)