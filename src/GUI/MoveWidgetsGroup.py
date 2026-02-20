
from PyQt5.QtWidgets import QWidget, QLabel,  QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


# Eva modifiers are the same as ACC_MODIFIERS inverted
ACC_MODIFIERS = [0.25, 0.28, 0.33, 0.40, 0.50, 0.66, 1.00, 1.50, 2.00, 2.50, 3.00, 3.50, 4.00]


class MoveStruct:
    """
    A small class to convert the move array into an object, to make it easier to handle. It contains the name, the type, power, accuracy, PP and the code of the move.

    Attributes:
        name (str): The name of the move.
        type (str): The type of the move.
        PP (int): The Power Points of the move.
        power (int): The power of the move.
        accuracy (int): The accuracy of the move.
        code (str): The code of the move.
    """
    def __init__(self,moveStruct:list):
        self.name=moveStruct[0]
        self.type=moveStruct[1]
        self.PP=moveStruct[2]
        self.power=moveStruct[3]
        self.accuracy=moveStruct[4] 
        self.code = moveStruct[5]

    def copy(self, source:'MoveStruct'):
        self.name=source.name
        self.type=source.type
        self.PP=source.PP
        self.power=source.power
        self.accuracy=source.accuracy
        self.code = source.code
    
    def updateMove(self, moveStruct:list):
        self.name=moveStruct[0]
        self.type=moveStruct[1]
        self.PP=moveStruct[2]
        self.power=moveStruct[3]
        self.accuracy=moveStruct[4] 
        self.code = moveStruct[5]

class MoveWidgetsGroup(QWidget):
    """
    A class made to group different widgets related to the moves. One instance account for a single move, and contains the move name, the PP and the type. The layout is horizontal, with the name on the left, then the power, PP. STAB moves are higlited, and the power is increased
    
    Attributes:        
        nameLabel (QLabel): The label displaying the move name.
        powLabel (QLabel): The label displaying the power of the move.
        precLabel (QLabel): The label displaying the accuracy of the move.
        PPLabel (QLabel): The label displaying the PP of the move.
        parent_types (tuple): The types of the Pokemon using the move, used to determine if the move is STAB or not.
        moveStruct (MoveStruct): The MoveStruct object containing the move's information, used to
    """

    def __init__(self, parent=None, parent_types=(), moveStruct:list=None):
        """
        Class constructor. Initialize the widgets in the group.

        :param parent: The parent widget of this MoveWidgetsGroup
        :param parent_types: The types of the Pokemon using the move, used to determine if the move is STAB or not
        :param moveStruct: The MoveStruct object containing the move's information
        """
        super().__init__(parent)
        self.parent_types = parent_types
        self.moveStruct = None
        # Create the labels for the move name, power, accuracy and PP
        self.nameLabel = self.create_label(200, Qt.AlignLeft)
        self.powLabel = self.create_label(80, Qt.AlignRight)
        self.precLabel = self.create_label(80, Qt.AlignRight)
        self.PPLabel = self.create_label(200, Qt.AlignLeft,QSizePolicy.Expanding)

        self.nameLabel.setText(self.moveStruct.name)

        # If move is a non-move placeholder, finish and do not setup the rest of the widgets
        if not self.moveStruct.name:
            return
        
        self.updateMove(self.moveStruct)
        

    def create_label(self, min_width, alignment=Qt.AlignLeft,policy=QSizePolicy.Preferred):
        """
        Creates a QLabel with the specified minimum width, alignment and size policy.
        """
        font = QFont("Sanserif", self.parent().textsize)
        label = QLabel()
        label.setFont(font)
        label.setMinimumWidth(min_width)
        label.setAlignment(alignment | Qt.AlignVCenter)
        label.setSizePolicy(policy, QSizePolicy.Preferred)
        return label
    
    #----

    def getWidgets(self):
        """
        Returns the widgets in the group as a list, in the order: move name, power, accuracy, PP.
        """
        return [self.nameLabel,self.powLabel,self.precLabel,self.PPLabel]
    
    #----
    def copymove(self, source:'MoveWidgetsGroup'):
        """
        Copies the move information and updates the widgets from another MoveWidgetsGroup instance. This is used when moves scale up in the list to copy the lower move's information to the upper move's widgets, to avoid having to fetch the move information again from the game. STAB is not recalculated, as it is assumed to be already computed.
        
        :param source: The MoveWidgetsGroup instance to copy the move information from.
        """
        
        self.moveStruct.copy(source.moveStruct)
        
        self.nameLabel.setText(source.nameLabel.text())
        self.nameLabel.setStyleSheet(source.nameLabel.styleSheet())

        self.powLabel.setText(source.powLabel.text())
        self.powLabel.setStyleSheet(source.powLabel.styleSheet())
        
        self.precLabel.setText(source.precLabel.text())     
        self.precLabel.setStyleSheet(source.precLabel.styleSheet())

        self.PPLabel.setText(source.PPLabel.text())
        self.PPLabel.setStyleSheet(source.PPLabel.styleSheet())

    def updateMove(self, moveStruct:list):
        """
        Updates the move information and the widgets from a MoveStruct object. This is used to update the move information when it changes in the game.

        :param moveStruct: The MoveStruct object containing the new move information.
        """
        if not self.moveStruct:
            self.moveStruct = MoveStruct(moveStruct)
        else:
            self.moveStruct.updateMove(moveStruct)

        if not self.moveStruct.name:
            # If move is a non-move placeholder, clear the widgets and finish
            self.nameLabel.setText("")
            self.powLabel.setText("")
            self.precLabel.setText("")
            self.PPLabel.setText("")
            return

        # Damage label setup, with STAB check
        if self.moveStruct.power > 0:
            # Damaging move, setup power and compute STAB
            power = int(self.moveStruct.power)
            if self.moveStruct.type == self.parent_types[0] or self.moveStruct.type == self.parent_types[1]:
                power = round(power * 1.5)
                self.nameLabel.setStyleSheet("color: rgb(0,255,0)")
                self.powLabel.setStyleSheet("color: rgb(0,255,0)")
                #self.PPLabel.setStyleSheet("color: rgb(0,255,0)")
                #self.precLabel.setStyleSheet("color: rgb(0,255,0)")
            else:
                self.nameLabel.setStyleSheet("color: white")
                self.powLabel.setStyleSheet("color: white")
                #self.PPLabel.setStyleSheet("color: white")
                #self.precLabel.setStyleSheet("color: white")
            self.powLabel.setText(str(power))
        else:
            self.powLabel.setText("-")
            self.nameLabel.setStyleSheet("color: white")
            self.powLabel.setStyleSheet("color: white")
            #self.PPLabel.setStyleSheet("color: white")
            #self.precLabel.setStyleSheet("color: white")
    
        # Accuracy label setup
        if self.moveStruct.accuracy > 0:
            self.precLabel.setText(str(self.moveStruct.accuracy))
        else: self.precLabel.setText("-")

        # PP label setup
        self.PPLabel.setText(f"  PP: {self.moveStruct.PP}/{self.moveStruct.PP}")

    def resetPrecision(self):
        """
        Resets the accuracy of the move to its original value. This is used when the move's accuracy is modified in the game, to reset it back to the original value when needed.
        """
        if self.moveStruct.code==0:
            return # If move is a non-move placeholder, do nothing
        self.precLabel
        self.precLabel.setText(str(self.moveStruct.accuracy) if self.moveStruct.accuracy < 99 else "-")
        self.precLabel.setStyleSheet("color:white")

    

    def updatePrecision(self, Eva:int, Acc:int):
        """
        Updates the accuracy of the move based on the given accuracy and evasion modifiers. This is used when the move's accuracy is modified in the game, to update the displayed accuracy accordingly. Precision label is colored green if the new accuracy is higher than the original, red if it is lower, and white if it is the same.

        :param Eva: The evasion modifier to apply to the move's accuracy.
        :param Acc: The accuracy modifier to apply to the move's accuracy.
        """
        if self.moveStruct.code == 0: return

        if self.moveStruct.accuracy == 0: return # If move has no accuracy, do nothing

        # If modifiers are out of bounds, set them to the default value of 8 (no modifier)
        if Acc < 1 or Acc > 15:
            Acc = 8
        if Eva < 1 or Eva > 15:
            Eva = 8
        # Compute accuracy based on move's base accuracy and the modifiers
        newPrec = round(self.moveStruct.accuracy*ACC_MODIFIERS[Acc-1]*ACC_MODIFIERS[-Eva],2)

        if newPrec > 99:
            self.precLabel.setText("-")
            return
        
        # Format newPrec: remove zero decimals, show integer if .0, else show up to 2 decimals
        if newPrec%1 ==0: # If newPrec is an integer, show it without decimals
            self.precLabel.setText(str(int(newPrec)))
        else:
            self.precLabel.setText(f"{newPrec:.2f}".rstrip('0').rstrip('.'))
        if newPrec > self.moveStruct.accuracy :
            color = "lime"
        elif newPrec < self.moveStruct.accuracy:
            color = "red"
        else:
            color = "white"
        self.precLabel.setStyleSheet(f"color:{color}")
        
    def updatePP(self, newPP):
        """
        Updates the PP of the move to the given value. This is used when the move's PP is modified in the game, to update the displayed PP accordingly.

        :param newPP: The new PP value to set for the move.
        """
        if self.moveStruct.code == 0: return # If move is a non-move placeholder, do nothing
        self.PPLabel.setText(f"  PP: {newPP}/{self.moveStruct.PP}")
