from math import sqrt
from PyQt5 import QtGui
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QApplication, QMenuBar, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QGridLayout, QGraphicsColorizeEffect,
    QGraphicsOpacityEffect, QSizePolicy,QFrame,QErrorMessage
)
from PyQt5.QtGui import QCloseEvent, QFont, QColor, QPixmap,QFontMetrics
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
import src.Twitch.TwitchNaturaController as TwitchNaturaController
from src.GameMonitorServer import GameMonitorServer

from GUI.MoveWidgetsGroup import MoveWidgetsGroup
from GUI.CounterWidget import CounterWidget
from GUI.SepLine import SepLine
from GUI.StatWidgetGroup import StatWidgetGroup, HpStatWidgetGroup, CritStatWidgetGroup
from configparser import ConfigParser
import json

class Natura(QMainWindow):
    twitchSignal = pyqtSignal(int, int)
    gameSignal = pyqtSignal(str, str)

    def __init__(self, name,config : ConfigParser):
        super(Natura, self).__init__()
        self.config = config
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
        self.makeTop()

       
       
    def makeName(self):
        self.nameLabel = QLabel("N°" + f"{self.NO:03d}" + " - " + self.name.upper())
        self.nameLabel.setFont(QFont("Sanserif", self.textsize+3))
        
        self.sepline_Top = SepLine()

        self.mainLayout.addWidget(self.nameLabel,alignment=Qt.AlignCenter)
        self.mainLayout.addWidget(self.sepline_Top)


    def makeTop(self):
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
        pass

    def makeBottom(self):
        pass


