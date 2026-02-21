from math import sqrt
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QWidget,  QHBoxLayout, QVBoxLayout,  QLabel, QGridLayout,  QSizePolicy
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from src.GUI.MoveWidgetsGroup import MoveWidgetsGroup
from src.GUI.CounterWidget import CounterWidget
from src.GUI.SepLine import SepLine
from src.GUI.StatWidgetGroup import StatWidgetGroup, HpStatWidgetGroup, CritStatWidgetGroup
from src.GUI.ScoreWidget import ScoreWidget
from configparser import ConfigParser

import json

class NaturaMainWindow(QMainWindow):
    twitchSignal = pyqtSignal(int, int)
    gameSignal = pyqtSignal(str, str)

    """Main window for the Natura application, which displays the stats and moves of a Pokémon.
    The window is divided into three sections: the top section displays the Pokémon's image,  level, experience, and types;
    the middle section displays the Pokémon's stats and  moves.
    The bottom section houses the current scoresfor the current run

    Attributes:
        config (ConfigParser): The configuration object containing the settings for the application.
        textsize (int): The size of the text used in the window.
        monitor (bool): A flag indicating whether the game monitor is enabled or not.
        twitch (bool): A flag indicating whether the Twitch integration is enabled or not.
        moves (list): A list of the Pokémon's moves, represented as tuples of (level, move data), where move data is a list containing the move's name, type, PP, power, precision and id.
        baseStats (list): A list of the Pokémon's base stats, in the order of HP, Attack, Defense, Speed, Special, and Crit%.
        types (list): A list of the Pokémon's types.
        NO (int): The Pokémon's National Dex number.
        name (str): The Pokémon's name.
        level (int): The Pokémon's current level, initialized to 5.
        version (str): The version of the application, used in the window title.

        mainLayout (QVBoxLayout): The main layout of the window, which contains all the other widgets and layouts.
        nameLabel (QLabel): A label displaying the Pokémon's name and National Dex number.
        image_label (QLabel): A label displaying the Pokémon's image.
        lvlabel (CounterWidget): A widget displaying the Pokémon's level, which can be incremented or decremented.
        expLabel (QLabel): A label displaying the Pokémon's current experience points, only shown if the game monitor is enabled.
        typeBox (QHBoxLayout): A horizontal layout containing the Pokémon's type icons.
        toplabelsLayout (QVBoxLayout): A layout containing the level and experience labels, as well as the type icons.
        
        statLayout (QGridLayout): A grid layout containing the Pokémon's stats, including HP, Attack, Defense, Speed, Special, and Crit%.
        hpWidget (HpStatWidgetGroup): A widget group for displaying the Pokémon's HP stat
        speedWidget (StatWidgetGroup): A widget group for displaying the Pokémon's Speed stat.
        attWidget (StatWidgetGroup): A widget group for displaying the Pokémon's Attack stat.
        defWidget (StatWidgetGroup): A widget group for displaying the Pokémon's Defense stat.
        specWidget (StatWidgetGroup): A widget group for displaying the Pokémon's Special stat.
        critWidget (CritStatWidgetGroup): A widget group for displaying the Pokémon's Crit% stat.
        StatWidget (QWidget): A widget containing the stat layout, which is added to the main layout.
        boostLabel (QLabel): A label displaying the maximum special stat boost at the current level, only shown if the game monitor is enabled.
        
        movesWidgets (list): A list of MoveWidgetsGroup instances for displaying the Pokémon's moves, initialized to a list of None values and populated in the makeMoves method.
        moveGrid (QGridLayout): A grid layout containing the move widgets, which is added to the main layout.
        nextMoveLabel (QLabel): A label displaying the next move to be learned, which is added to the main layout.

        avoided (CounterWidget): A widget for tracking the number of skipped trainers.
        selv (CounterWidget): A widget for tracking the number of wild pokemon faced.
        finalScore (ScoreWidget): A widget for displaying the current score of the run

    """

    def __init__(self, name,config : ConfigParser,version : str):
        super(NaturaMainWindow, self).__init__()
        self.config = config
        self.version = version
        self.mainLayout = QVBoxLayout()

        self.textsize = self.config.getint("MAIN", "DIM_TESTO")
        self.monitor = self.config.getboolean("MAIN", "USE_MGBA")
        self.twitch = self.config.getboolean("MAIN", "USE_TWITCH")

        with open(f"data/mons_json/{name}.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            self.moves=[ (int (i[0]), i[1]) for i in data["level_up_moves"]]
            self.baseStats = data["base_stats"]
            self.types = data["types"]
            self.NO = data["NO"]
            self.name = data["name"]
            if self.monitor:
                self.expclass = int(data["expected_level"][1])
            else: self.expclass = int(data["expected_level"][0])
        
        self.level = 5
        self.makeName()
        self.makeTop()
        self.makeStats()
        self.makeMoves()
        self.makeBottom()

        self.setWindowTitle(f"Natura Challenge - {self.version}")
        self.setWindowIcon(QtGui.QIcon('data/nature.png'))
        self.setStyleSheet("background-color: black;  color:white;border: white;font-family:Pokemon GB")
        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)

        if self.twitch:
            import src.Twitch.TwitchNaturaController as TwitchNaturaController
            self.twitchController = TwitchNaturaController.TwitchNaturaController(self.twitchSignal,self.config)
            self.twitchSignal.connect(self.twitchController.twitchUpdate)
            self.twitchController.start()
        
        if self.monitor:
            from src.GameMonitorServer import GameMonitorServer
            self.battleSwitch = False
            self.gameSignal.connect(self.gameUpdate)
            self.gameMonitor = GameMonitorServer(self.gameSignal,self.config)
            self.gameMonitor.start()

       
       
    def makeName(self):
        self.nameLabel = QLabel("N°" + f"{self.NO:03d}" + " - " + self.name.upper())
        self.nameLabel.setFont(QFont("Sanserif", self.textsize+3))
        
        sepline_Top = SepLine()

        self.mainLayout.addWidget(self.nameLabel,alignment=Qt.AlignCenter)
        self.mainLayout.addWidget(sepline_Top)


    def makeTop(self):
        """
        Make the top section of the window, which includes the image, level, experience, and types.
        """
        # --- Top Section ---

        # Image and LV

        self.image_label = QLabel()
        pixmap = QPixmap("data/sprites/" +  f"{self.NO:04d}" + ".png")
        self.image_label.setPixmap(pixmap)

        self.lvlabel=CounterWidget(self,"LV:",self.textsize,self.textsize,5)
        self.lvlabel.setFont(QFont("Sanserif", self.textsize))

        self.topLabelsLayout = QVBoxLayout()
        self.topLabelsLayout.addStretch(1)
        self.topLabelsLayout.addWidget(self.lvlabel)

        # --- EXP ---
        if self.monitor:
            self.exp=0
            self.expLabel = QLabel("Exp: "+str(self.exp))
            self.expLabel.setFont(QFont("Sanserif", self.textsize))
            self.topLabelsLayout.addWidget(self.expLabel)

        # --- Types ---
        self.typeBox=QHBoxLayout()
        typeWidget=QWidget()

        type1Label = QLabel()
        type1Pix = QPixmap("data/sprites/" +  self.data["types"][0] + ".png")
        type1Pix=type1Pix.scaledToHeight(25)
        type1Label.setPixmap(type1Pix)
        self.typeBox.addWidget(type1Label)
        
        if self.types[0] != self.types[1]:
            type2label = QLabel()
            type2Pix = QPixmap("data/sprites/" +  self.data["types"][1] + ".png")
            type2Pix=type2Pix.scaledToHeight(25)
            type2label.setPixmap(type2Pix)
            self.typeBox.addWidget(type2label)
        
        typeWidget.setLayout(self.typeBox)
        self.topLabelsLayout.addWidget(typeWidget)
        self.topLabelsLayout.addStretch(1)

        self.top_layout = QHBoxLayout()
        self.top_layout.addWidget(self.image_label)
    
        self.top_layout.addStretch(1)
        self.top_layout.addLayout(self.topLabelsLayout)
        self.top_layout.addStretch(1)

        self.mainLayout.addLayout(self.top_layout)
        self.mainLayout.addWidget(SepLine())


    
    def makeStats(self):
        """
        Make the stats section of the window, which includes HP, Attack, Defense, Speed, Special, and Crit.
        """
        self.statLayout = QGridLayout()
        self.statLayout.setContentsMargins(0, 0, 0, 0)

        # HP
        self.hpWidget = HpStatWidgetGroup(self, self.baseStats[0])
        label, value, modifiers = self.hpWidget.getWidgets()
        self.statLayout.addWidget(label, 0, 0)
        self.statLayout.addWidget(value, 0, 1)
        if self.monitor:
            self.statLayout.addWidget(modifiers, 0, 2)

        # SPEED
        self.speedWidget = StatWidgetGroup(self, "VEL.", self.baseStats[3])
        label, value, modifiers = self.speedWidget.getWidgets()
        self.statLayout.addWidget(label, 0, 3)
        self.statLayout.addWidget(value, 0, 4)
        if self.monitor:
            self.statLayout.addWidget(modifiers, 0, 5)

        #   ATTACK
        self.attWidget = StatWidgetGroup(self, "ATT.", self.baseStats[1])
        label, value, modifiers = self.attWidget.getWidgets()
        self.statLayout.addWidget(label, 1, 0)
        self.statLayout.addWidget(value, 1, 1)
        if self.monitor:
            self.statLayout.addWidget(modifiers, 1, 2)

        #   DEFENSE
        self.defWidget = StatWidgetGroup(self, "DEF.", self.baseStats[2])
        label, value, modifiers = self.defWidget.getWidgets()
        self.statLayout.addWidget(label, 1, 3)
        self.statLayout.addWidget(value, 1, 4)
        if self.monitor:
            self.statLayout.addWidget(modifiers, 1, 5)

        #   SPECIALS
        self.sepcWidget = StatWidgetGroup(self, "SPEC.", self.baseStats[4])
        label, value, modifiers = self.sepcWidget.getWidgets()
        self.statLayout.addWidget(label, 2, 0)
        self.statLayout.addWidget(value, 2, 1)
        if self.monitor:
            self.statLayout.addWidget(modifiers, 2, 2)

        # CRIT
        self.critWidget = CritStatWidgetGroup(self, self.baseStats[5], self.level)
        label, value, modifiers = self.critWidget.getWidgets()
        self.statLayout.addWidget(label, 2, 3)
        self.statLayout.addWidget(value, 2, 4)
        self.statLayout.addWidget(value, 2, 5)

        self.StatWidget = QWidget()
        self.StatWidget.setLayout(self.statLayout)
        self.mainLayout.addWidget(self.StatWidget)

        if self.monitor:
            self.boostLabel=QLabel("Boost Stat. Esp. Massimo: +"+str(int(63*(self.level/100))))
            self.boostLabel.setFont(QFont("Sanserif", self.textsize-3))

        self.mainLayout.addWidget(self.boostLabel)

        

    def makeMoves(self):
        """
        Make the moves section of the window, which includes the move names, types, and PP.
        Also add a lavel for the next move to be learned.
        """
        self.movesWidgets = [None]*4

        self.moveGrid = QGridLayout()
        self.moveGrid.setSpacing(5)
        for i in range(4):
            moveWidget = MoveWidgetsGroup(self, self.types,self.moves[i][1])
            self.movesWidgets[i] = moveWidget
            name, power, precision, pp = moveWidget.getWidgets()
            self.moveGrid.addWidget(name, i, 0)
            self.moveGrid.addWidget(power, i, 1)
            self.moveGrid.addWidget(precision, i, 2)
            self.moveGrid.addWidget(pp, i, 3)
        
        if len(self.moves)>4:
            self.nextMoveLabel = QLabel(f"Prossima: {self.moves[4][1][0]} ({self.moves[4][0]})")
        else : self.nextMoveLabel = QLabel("Prossima: ---")
        self.nextMoveLabel.setAlignment(Qt.AlignLeft)
        self.nextMoveLabel.setFont(QFont("Sanserif", self.textsize))
        self.nextMoveLabel.setStyleSheet("background-color: black; color: white; border: black;")
        self.nextMoveLabel.setMinimumWidth(150)
        
        self.mainLayout.addWidget(self.moveGrid)
        self.mainLayout.addWidget(SepLine(2,"dasehd"))
        self.mainLayout.addWidget(self.nextMoveLabel)
        self.mainLayout.addWidget(SepLine())
        

    def makeBottom(self):
        """
        Make the bottom section of the window, which includes the current scores for the run.
        """

        self.avoided = CounterWidget(self,"EVIT:",self.textsize,self.textsize)
        self.avoided.setMinimumSize(160,20)
        self.avoided.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        self.selv = CounterWidget(self,"SELV:",self.textsize,self.textsize)
        self.selv.setMinimumSize(160,20)
        self.selv.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        self.finalScore = ScoreWidget(self,"PUNTEGGIO:",self.textsize,self.textsize)

        self.counterLayout = QVBoxLayout()
        self.counterLayout.setContentsMargins(0, 0, 0, 0)
        self.counterLayout.addWidget(self.avoided, alignment=Qt.AlignLeft)
        self.counterLayout.addWidget(self.selv,alignment=Qt.AlignLeft)
        self.counterLayout.addStretch(1)
        self.counterLayout.addWidget(self.finalScore)

        bottomWidget = QWidget()
        bottomWidget.setLayout(self.counterLayout)
        self.mainLayout.addWidget(bottomWidget)