
from PyQt5.QtWidgets import QWidget, QLabel,  QSizePolicy, QHBoxLayout
from PyQt5.QtCore import Qt
from math import sqrt
class StatStruct:
    """ 
    A small class representing a pokemon stat.

    Attributes:
        name (str): The name of the stat.
        battle_stat (int): The stats during battle.
        actual_value (int): The stat outside the battle.
        modifier (int): The current modifier of the stat, from -6 to +6.
        stat_exp (int): The experience of the stat
    """
    def __init__(self,name:str, base_value:int):
        """
        Class constructor. Initializes the stat with the given name, base value and modifier.
            
        :param name: The name of the stat.
        :param base_value: The base value of the stat.
        :param modifier: The current modifier of the stat, from -6 to +6."""
        self.name=name
        self.battle_stat=base_value
        self.actual_value = base_value
        self.stat_exp=0

    def reset_stat(self):
        """
        Resets the stat modifier to 0 and the actual value to the base value.         """
        self.actual_value=self.battle_stat

    def update(self, battle_value:int, current_value:int ,stat_exp:int):
        """
        Updates the values of this StatStruct object from a list representation. This is used to update the stat information when it changes in the game.

        :param battle_value: The value of the stat during battle.
        :param current_value: The new current value.
        :param stat_exp: The new stat experience value.
        """
        self.battle_stat = battle_value
        self.actual_value = current_value
        self.stat_exp = stat_exp


stat_reorder_dict = {0:0, 1:3, 2:2, 3:4, 4:2}


class StatWidgetGroup(QWidget):
    """
    A class made to group different widgets related to the stats. 
    One instance account for a single stat, and contains the stat name, its value and the stat exp modifier. 
    The layout is horizontal, with the name on the left, then the current value and then the modifier.
    
    Attributes:
        nameLabel (QLabel): The label displaying the stat name.
        currentLabel (QLabel): The label displaying the current value of the stat.
        additionalLabel (QLabel): The label displaying the modifier of the stat.
    """


    def __init__(self, parent=None, name=None, base_value=None):
        """
        Class constructor. Initialize the widgets in the group.

        :param parent: The parent widget of this StatWidgetsGroup
        :param name: The name of the stat to display in the nameLabel.
        :param base_value: The base value of the stat to display in the currentLabel.

        """
        super().__init__(parent)
        self.statStruct = StatStruct(name, base_value)

        # Create the labels for the stat name, current value and modifier
        self.nameLabel = QLabel(self.statStruct.name)
        self.nameLabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.nameLabel.setStyleSheet("background-color: black; border:black; color:white;font-family:Pokemon GB")                    
        self.nameLabel.setMinimumWidth(self.nameLabel.sizeHint().width())
        self.nameLabel.setAlignment(Qt.AlignLeft)

        self.valueLabel = QLabel(f"{self.statStruct.actual_value}")
        self.valueLabel.setStyleSheet("background-color: black; border: black; color:white")
        self.valueLabel.setMinimumWidth(100)
        self.valueLabel.setAlignment(Qt.AlignLeft)

        self.additionalLabel = QLabel(f"(+0)")
        self.additionalLabel.setStyleSheet("background-color: black; border: black; color:white")
        self.additionalLabel.setMinimumWidth(100)
        self.additionalLabel.setAlignment(Qt.AlignRight)

            
    #----

    def getWidgets(self):
        """
        Returns the widgets in the group as a list, in the order: stat name, current value, modifier.
        """
        return [self.nameLabel, self.valueLabel, self.additionalLabel]
    
   

    def updateStat(self, current_value:int,OOB_value:int, stat_exp:int, level:int):
        """
        Updates the stat information and the widgets from a list representation. This is used to update the stat information when it changes in the game.

        :param current_value: The new current value of the stat.
        :param OOB_battle_value: The new out-of-battle value of the stat.
        :param stat_exp: The new stat experience value of the stat.
        """
        
        self.statStruct.update(OOB_value, current_value, stat_exp)

        self.valueLabel.setText(f"{self.statStruct.actual_value}")

        stat_exp_mod = int((int(sqrt(stat_exp-1)+1)*level)/400)
        self.additionalLabel.setText(f"({stat_exp_mod:+d})")
        if stat_exp >= 65535:
            self.additionalLabel.setStyleSheet("color: lime")
        if current_value > OOB_value:
            self.valueLabel.setStyleSheet("color: lime")
        elif current_value < OOB_value:
            self.valueLabel.setStyleSheet("color: red")
        else:
            self.valueLabel.setStyleSheet("color: white")
        

class HpStatWidgetGroup(StatWidgetGroup):
    """
    Specialization of StatWidgetGroup for the HP stat.
    This class inherits from StatWidgetGroup and is used specifically for the HP stat.
    """

    def __init__(self, parent=None, basevalue:int=None):
        """
        Class constructor. Initializes the widgets in the group for the HP stat.

        :param parent: The parent widget of this HpStatWidgetGroup
        :param name: The name of the stat to display in the nameLabel.
        :param base_value: The base value of the stat to display in the currentLabel.

        """
        super().__init__(parent, "PS", basevalue)
        self.valueLabel.setText(f"{self.statStruct.actual_value}/{self.statStruct.battle_stat}")


    def updateStat(self, current_value:int,OOB_value:int, stat_exp:int, level:int):
        """
        Updates the HP stat information and the widgets from a list representation. This is used to update the HP stat information when it changes in the game.

        :param current_value: The new current value of the HP stat.
        :param OOB_battle_value: The new out-of-battle value of the HP stat.
        :param modifier: The new modifier value of the HP stat.
        :param stat_exp: The new stat experience value of the HP stat.
        """
        super().updateStat(current_value, OOB_value, 0, stat_exp, level)
        color = "white"
        if current_value < OOB_value:
            color = "red"
        self.valueLabel.setText(f"<font color='{color}'>{self.statStruct.actual_value}</font>/{self.statStruct.battle_stat}</font>")


class CritStatWidgetGroup(StatWidgetGroup):
    """
    Specialization of StatWidgetGroup for the critical hit stat.
    This class inherits from StatWidgetGroup and is used specifically for the critical hit stat.
    """

    def __init__(self, parent=None, basevalue:float=None, level:int=None):
        """
        Class constructor. Initializes the widgets in the group for the critical hit stat.  
        """
        super().__init__(parent, "%CRIT", basevalue)
        
        modifier = round((2*level+5)/(level+5),2)
        self.additionalLabel.setText(f"X{modifier:.2f}%")
        
        # Second label for HCR moves
        self.seconAdditionalLabel = QLabel(f"X{min(modifier*8, 99.6):.2f}%")
        self.seconAdditionalLabel.setStyleSheet("background-color: black; border: black; color:white")
        self.seconAdditionalLabel.setMinimumWidth(100)
        self.seconAdditionalLabel.setAlignment(Qt.AlignRight)

        self.addLayout = QHBoxLayout()
        self.addLayout.addWidget(self.additionalLabel)
        self.addLayout.addWidget(self.seconAdditionalLabel)

        self.ModifiersWidget= QWidget()
        self.ModifiersWidget.setStyleSheet("background-color: black; border: black; color:white")
        self.ModifiersWidget.setLayout(self.addLayout)

    def getWidgets(self):
        """
        Returns the widgets in the group as a list, in the order: stat name, current value, modifier, second modifier.
        """
        return [self.nameLabel, self.valueLabel, self.ModifiersWidget]
    

    def updateStat(self, level):
        modifier = round((2*level+5)/(level+5),2)
        self.additionalLabel.setText(f"X{modifier:.2f}%")
        self.seconAdditionalLabel.setText(f"X{min(modifier*8, 99.6):.2f}%")