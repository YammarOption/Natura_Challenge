from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class ScoreWidget(QWidget):
    """
    A simple counter widget that displays a label and a value, with the value's color changing based on its magnitude. Starting value is set to 100.000.
    
    Attributes:
        textLabel (QLabel): The label displaying the counter's name.
        value_label (QLabel): The label displaying the counter's value.
        layout (QHBoxLayout): The layout containing the labels.
    """
    def __init__(self, label_text, text_size=12, num_size=12):
        """
        Class constructor

        :param label_text: The text to display on the label
        :param text_size: The size of the label text    
        """
        super().__init__()

        # Text label setup
        self.textLabel = QLabel(label_text)
        self.textLabel.setWordWrap(True)
        self.textLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.textLabel.setStyleSheet("background-color: black; border: black; color:white")
        self.textLabel.setFont(QFont("Sanserif", text_size+5))

        # Value label setup
        self.value_label = QLabel("100.000")
        self.value_label.setMinimumWidth(60)
        self.value_label.setAlignment(Qt.AlignCenter)
        
        color = f"rgb({0},{255},0)"
        self.value_label.setStyleSheet(
            f"background-color: black; border: black; color: {color}"
        )
        self.value_label.setFont(QFont("Sanserif", num_size+5))

        # Main layout
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(30)
        self.layout.addWidget(self.textLabel)
        self.layout.addWidget(self.value_label)
        self.layout.addStretch(1)
        self.setLayout(self.layout)

    def set_count(self, value):
        """
        Update the counter's value and adjust the color based on the value's magnitude. Values above 100 are displayed in green, while values below 100 transition towards red as they decrease.
        """
        if value >= 100:
            # No values over 100 allowed
            value = 100
            self.value_label.setText(f"{value:0,.3f}")
        else: self.value_label.setText(f"{value:0,.3f}")

        # Ensure colors are always bright enough (avoid dark colors)
        min_brightness = 120
        red = int(min_brightness + (255 - min_brightness) * (1 - value / 100))
        green = int(min_brightness + (255 - min_brightness) * (value / 100))
        color = f"rgb({red},{green},0)"
        self.value_label.setStyleSheet(
            f"background-color: black; border: black; color: {color}"
        )