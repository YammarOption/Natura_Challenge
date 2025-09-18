from math import sqrt
from PyQt5 import QtGui
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QApplication, QMenuBar, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QGridLayout, QGraphicsColorizeEffect,
    QGraphicsOpacityEffect, QSizePolicy,QFrame
)
from PyQt5.QtGui import QCloseEvent, QFont, QColor, QPixmap,QFontMetrics
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
import src.Twitch.TwitchNaturaController as TwitchNaturaController
from src.GameMonitorServer import GameMonitorServer
import configparser
import json

ACC_MODIFIERS = [0.25, 0.28, 0.33, 0.40, 0.50, 0.66, 1.00, 1.50, 2.00, 2.50, 3.00, 3.50, 4.00]
# Eva modifiers are the same as ACC_MODIFIERS inverted
#EVA_MODIFIERS = [0.25, 0.28, 0.33, 0.40, 0.50, 0.66, 1.00, 1.50, 2.00, 2.50, 3.00, 3.50, 4.00]

class SepLine(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)
        self.setStyleSheet("border: 3px solid white;")
        
class CounterWidget(QWidget):
    def __init__(self, parent, label_text, text_size=12, font_size=12,count=0,islevel=False):
        QtGui.QFontDatabase.addApplicationFont("data/Pokemon GB.ttf")
        super().__init__()
        self.Mainparent= parent
        self.count = count
        self.isLevel=islevel
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        self.label = QLabel(label_text)
        self.label.setWordWrap(True)
        if not self.isLevel: self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.value_label = QLabel(str(self.count))
        self.label.setStyleSheet("background-color: black; border:black; color:white")
        self.label.setFont(QFont("Sanserif", text_size))

        self.value_label.setStyleSheet("background-color: black; border: black; color:white")
        self.label.setMinimumWidth(50)
        self.value_label.setMinimumWidth(50)
        self.value_label.setAlignment(Qt.AlignRight)
        self.label.setAlignment(Qt.AlignLeft)
        self.value_label.setFont(QFont("Sanserif", font_size))
        
        
        layout.addWidget(self.label)
        self.btn_inc = QPushButton('+')
        self.btn_inc.clicked.connect(self.increase)
        if not self.isLevel:
            self.btn_dec = QPushButton('-')
            self.btn_dec.clicked.connect(self.decrease)
            layout.addWidget(self.btn_dec)
        layout.addWidget(self.value_label)
        layout.addWidget(self.btn_inc)
        if self.isLevel:layout.addStretch(1)

        self.setLayout(layout)

    def increase(self):
        self.count += 1
        self.value_label.setText(str(self.count))
        self.Mainparent.updateScore(levelUp=self.isLevel)

    def decrease(self):
        self.count = max(0, self.count -1)
        self.value_label.setText(str(self.count))
        self.Mainparent.updateScore(levelUp=self.isLevel)

    def get_count(self):
        return self.count

    def set_count(self, value):
        self.count = value
        self.value_label.setText(str(self.count))
        

class SimpleCounter(QWidget):
    def __init__(self, label_text, text_size=12, num_size=12):
        super().__init__()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        self.label = QLabel(label_text)
        self.label.setWordWrap(True)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.value_label = QLabel("100.0")
        self.value_label.setMinimumWidth(60)
        self.value_label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("background-color: black; border: black; color:white")
        self.label.setFont(QFont("Sanserif", text_size+5))
        
        color = f"rgb({0},{255},0)"
        self.value_label.setStyleSheet(
            f"background-color: black; border: black; color: {color}"
        )
        self.value_label.setFont(QFont("Sanserif", num_size))

        layout.addWidget(self.label)
        layout.addWidget(self.value_label)
        layout.addStretch(1)
        self.setLayout(layout)

    def set_count(self, value):
        #print(value)
        if value >= 100:
            self.value_label.setText(f"{value:0,.1f}")
        else: self.value_label.setText(f"{value:0,.2f}")
        # Ensure colors are always bright enough (avoid dark colors)
        min_brightness = 120
        red = int(min_brightness + (255 - min_brightness) * (1 - value / 100))
        green = int(min_brightness + (255 - min_brightness) * (value / 100))
        color = f"rgb({red},{green},0)"
        #print(color)
        self.value_label.setStyleSheet(
            f"background-color: black; border: black; color: {color}"
        )
#border: 1px solid white
#border: black


class movebox():
    def __init__(self, parent, parentTypes):
        super().__init__()
        self.Mainparent = parent
        self.parentTypes = parentTypes

    def getWidgets(self,moveArray):
        self.name = moveArray[0]
        self.type = moveArray[1]
        self.code = moveArray[5]

        #layout = QHBoxLayout()
        #layout.setContentsMargins(5, 0, 5, 0)
        #layout.setSpacing(15)
        self.movelabel = self.create_label(200, Qt.AlignLeft)
        self.movelabel.setText(self.name)
        self.powLevel = self.create_label(80, Qt.AlignRight)
        self.precLabel = self.create_label(80, Qt.AlignRight)
        self.PPLabel = self.create_label(200, Qt.AlignLeft,QSizePolicy.Expanding)

        # Header row (empty name)
        if self.name == "":
            return (
            self.movelabel,
            self.powLevel,
            self.precLabel,
            self.PPLabel)

        # Power
        if moveArray[3] > 0:
            power = int(moveArray[3])
            if self.type == self.parentTypes[0] or self.type == self.parentTypes[1]:
                power = round(power * 1.5)
                self.movelabel.setStyleSheet("color: rgb(0,255,0)")
            self.powLevel.setText(str(power))
        else:
            self.powLevel.setText("-")

        # Precision
        self.prec=moveArray[4]
        self.precLabel.setText(str(int(moveArray[4])) if moveArray[4] > 0 else "-")

        # PP
        self.maxPP = int(moveArray[2])
        self.PPLabel.setText(f"  PP: {self.maxPP}/{self.maxPP}")

        return (
            self.movelabel,
            self.powLevel,
            self.precLabel,
            self.PPLabel)
        #self.setLayout(layout)
        #self.setMinimumHeight(30)  # Optional: unify row height


    def create_label(self, min_width, alignment=Qt.AlignLeft,policy=QSizePolicy.Preferred):
        font = QFont("Sanserif", self.Mainparent.textsize)
        label = QLabel()
        label.setFont(font)
        label.setMinimumWidth(min_width)
        label.setAlignment(alignment | Qt.AlignVCenter)
        label.setSizePolicy(policy, QSizePolicy.Preferred)
        return label

    def updatePP(self,PPcount):
        if self.code == 0: return
        self.PPLabel.setText("  PP: "+str(PPcount)+"/"+str(self.maxPP))
    
    def updatePrec(self, Eva, Acc):
        if self.code == 0: return
        newPrec = round(self.prec*ACC_MODIFIERS[Acc-1]*ACC_MODIFIERS[-Eva],2)
   #     print(f"Acc: {Acc}, Prec: {self.prec}, ACC_MODIFIERS[Acc-1]: {ACC_MODIFIERS[Acc-1]}, ACC_MODIFIERS[-Eva]: {ACC_MODIFIERS[-Eva]}, newPrec: {newPrec}")
        # Format newPrec: remove zero decimals, show integer if .0, else show up to 2 decimals
        if newPrec <= 100:
            if newPrec == int(newPrec):
                self.precLabel.setText(str(int(newPrec)))
            else:
                self.precLabel.setText(f"{newPrec:.2f}".rstrip('0').rstrip('.'))
        else:
            self.precLabel.setText("-")
        if newPrec > self.prec :
            color = "lime"
        elif newPrec < self.prec:
            color = "red"
        else:
            color = "white"
        self.precLabel.setStyleSheet(f"color:{color}")

    def resetPrec(self):
        if self.code == 0: return
        self.precLabel.setText(str(self.prec) if self.prec <= 100 else "-")
        self.precLabel.setStyleSheet("color:white")

    def updateMove(self,moveArray):
        self.name=moveArray[0]
        self.type = moveArray[1]
        self.movelabel.setText(self.name)
        if moveArray[3]>0:
            power = int(moveArray[3])
            if self.type == self.parentTypes[0] or moveArray[1] == self.parentTypes[1]:
                power=round(power*1.5)
                self.movelabel.setStyleSheet("color: rgb(0,255,0)")
            else: self.movelabel.setStyleSheet("color: white")
            self.powLevel.setText(str(power))
        else :
            self.powLevel.setText("-")
            self.movelabel.setStyleSheet("color: white")

        if moveArray[4]>0:
            prec = int(moveArray[4])
            self.prec=prec
            self.precLabel.setText(str(prec))
        else : 
            self.precLabel.setText("-")
            self.precLabel.setStyleSheet(f"color:white")
        self.code=moveArray[5]
        self.maxPP = int(moveArray[2])
        self.PPLabel.setText("  PP: "+str(self.maxPP)+"/"+str(self.maxPP))

    def copymove(self, source: 'movebox'):
        self.name=source.name
        self.type=source.type
        self.code=source.code
        self.movelabel.setText(source.movelabel.text())
        self.powLevel.setText(source.powLevel.text())
        if source.powLevel.text() != "-" and (self.type == self.parentTypes[0] or self.type == self.parentTypes[1]):
            self.movelabel.setStyleSheet("color: rgb(0,255,0)")
        else :self.movelabel.setStyleSheet("color:white")
        self.prec=source.prec
        self.precLabel.setText(source.precLabel.text())     
        self.maxPP = source.maxPP
        self.PPLabel.setText(source.PPLabel.text())


class Natura(QMainWindow):
    twitchSignal = pyqtSignal(int, int)
    gameSignal = pyqtSignal(str, str)

    def __init__(self, mon_name):
        super(Natura, self).__init__()
        self.name = mon_name
        self.mv = [None] * 4  # 4 moves
        self.monstats = [None] * 6  # 5 stats + crit

    def setup(self, config: configparser.ConfigParser):
        main_layout = QVBoxLayout()
        self.config = config
        self.textsize = self.config.getint("MAIN", "DIM_TESTO")
        self.monitor = self.config.getboolean("MAIN", "USE_MGBA")
        self.twitch = self.config.getboolean("MAIN", "USE_TWITCH")
        with open(f"data/mons_json/{self.name}.json", "r", encoding="utf-8") as f:
            self.data = json.load(f)
        self.moves=[ (int (i[0]), i[1]) for i in self.data["level_up_moves"]]
        self.maxlevel=int(self.data["expected_level"][0])
        self.maxexp=int(self.data["expected_level"][1])
        # --- Top Section ---
        label1 = QLabel("N°" + f"{self.data['NO']:03d}" + " - " + self.data["name"].upper())
        label1.setFont(QFont("Sanserif", self.textsize+3))
        main_layout.addWidget(label1,alignment=Qt.AlignCenter)
        line = SepLine()
        main_layout.addWidget(line)

        
        top_layout = QHBoxLayout()
        image_label = QLabel()
        pixmap = QPixmap("data/sprites/" +  f"{self.data['NO']:04d}" + ".png")
        image_label.setPixmap(pixmap)
        top_layout.addWidget(image_label)

        label_container = QVBoxLayout()
        if self.monitor:
            self.lvlabel=CounterWidget(self,"LV:",self.textsize,self.textsize,1,islevel=True)
        else: self.lvlabel=CounterWidget(self,"LV:",self.textsize,self.textsize,5,islevel=True)
        self.lvlabel.setFont(QFont("Sanserif", self.textsize))
        label_container.addStretch(1)
        label_container.addWidget(self.lvlabel)
        if self.monitor:
            self.exp=0
            self.expLabel = QLabel("Exp: "+str(self.exp))
            self.expLabel.setFont(QFont("Sanserif", self.textsize))
            label_container.addWidget(self.expLabel)
        typelabel = QLabel()
        if self.data["types"][0] == self.data["types"][1]:
            typelabel.setText("TIPO1 "+ self.data["types"][0])
        else :
            typelabel.setText("TIPO1 "+self.data["types"][0]+"\n\nTIPO2 "+self.data["types"][1])
        typelabel.setFont(QFont("Sanserif", self.textsize))
        label_container.addWidget(typelabel)
    
        label_container.addStretch(1)
        top_layout.addStretch(1)
        top_layout.addLayout(label_container)
        top_layout.addStretch(1)

        main_layout.addLayout(top_layout)
        main_layout.addWidget(SepLine())

        # --- Middle Section ---
        middle_layout = QVBoxLayout()
        # sats
        statgrid = QGridLayout()
        statgrid.setContentsMargins(0, 0, 0, 0)
        #statgrid.setSpacing(1)
        statslabels=["PS   ","VEL. ","ATT.","SPEC.","DIF.","%CRIT"]
        value_indices = [0, 3, 1, 4, 2, 5]
        for i in range(3):
            for j in range(0,6,3):
                    label = QLabel(statslabels[i * 2 + int(j/2)])
                    #label.setWordWrap(True)
                    label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
                    label.setStyleSheet("background-color: black; border:black; color:white;font-family:Pokemon GB")                    
                    label.setMinimumWidth(label.sizeHint().width())

                    # Map index to value index: 0->0, 1->3, 2->2, 3->4, 4->2
                    value_index = value_indices[i * 2 + int(j/2)]
                    if (i*2+int(j/2) == 5):
                        value = self.data["base_stats"][value_index]
                        value_label = QLabel(f"{value}")
                        if self.monitor: statExp_label = QLabel(f"(X{round((2*self.lvlabel.get_count()+5)/(self.lvlabel.get_count()+5),2)})")
                    else:
                        if self.monitor: 
                            value_label = QLabel(str(self.data["base_stats"][value_index]))
                            statExp_label=QLabel("(+0)")
                        else:
                            value_label = QLabel(str(self.data["base_stats"][value_index]))
                    label.setFont(QFont("Sanserif", self.textsize))
                    value_label.setStyleSheet("background-color: black; border: black; color:white")
                    value_label.setMinimumWidth(100)
                    #label.setMinimumWidth(50)
                    value_label.setAlignment(Qt.AlignRight)
                    label.setAlignment(Qt.AlignLeft)
                    value_label.setFont(QFont("Sanserif", self.textsize))
                    #layout.addStretch(1)
                    statgrid.addWidget(label,i,j,alignment=Qt.AlignLeft)

                    if self.monitor:
                        statgrid.addWidget(value_label,i,j+1,alignment=Qt.AlignRight)
                        statExp_label.setMinimumWidth(100)
                        statExp_label.setAlignment(Qt.AlignRight)
                        statExp_label.setFont(QFont("Sanserif", self.textsize))
                        statgrid.addWidget(statExp_label,i,j+2,alignment=Qt.AlignRight)
                        self.monstats[i*2  + int(j/2)] = (value_label,statExp_label)
                        self.boostLabel=QLabel("Boost Stat. Esp. Massimo: +"+str(int(63*(self.lvlabel.get_count()/100))))
                        self.boostLabel.setFont(QFont("Sanserif", self.textsize-3))
                    else:
                        statgrid.addWidget(value_label,i,round(j+1/2)+1,alignment=Qt.AlignRight)
                        self.monstats[i*2  + int(j/2)] = (value_label,None)
        middle_layout.addLayout(statgrid)
        if self.monitor:
            middle_layout.addWidget(self.boostLabel)

        middle_layout.addWidget(SepLine())
        movelayout = QGridLayout()
        #movebox.setContentsMargins(0, 0, 0, 0)
        movelayout.setSpacing(5)
        #moves
        currmoves={}
        for i in range(4):
                #print(self.moves[i*2+j][1][0])
                currmoves[self.moves[i][1][0]]=self.moves[i][1]
                self.mv[i] = movebox(self,self.data["types"])
                (name,pow,prec,pp) = self.mv[i].getWidgets(self.moves[i][1])
                for j, label in enumerate((name, pow, prec, pp)):
                    movelayout.addWidget(label, i, j)

        middle_layout.addLayout(movelayout)
        if len(self.moves)>4:
            self.next = QLabel("PROSSIMA: "+f"{self.moves[4][1][0]} ({self.moves[4][0]})")
        else :self.next = QLabel("PROSSIMA: --")
        self.next.setAlignment(Qt.AlignLeft)
        self.next.setFont(QFont("Sanserif", self.textsize))
        self.next.setStyleSheet("background-color: black; color: white; border: black;")
        self.next.setMinimumWidth(150)

        middle_layout.addWidget(self.next)

        main_layout.addLayout(middle_layout)
        main_layout.addWidget(SepLine())

        # --- Bottom Section ---
        bottom_layout = QVBoxLayout()
        bottom_layout.addStretch(1)
        counter_grid = QGridLayout()
        counter_grid.setContentsMargins(0, 0, 0, 0)
        #counter_grid.setSpacing(1)
        labels = ["RESET", "EXTRA", "EVIT.", "SELV."]
        self.stats=[None]*4
        for i in range(2):
            for j in range(2):
                counter = CounterWidget(self,labels[i * 2 + j], self.textsize, self.textsize)
                counter.setMinimumSize(160, 20)
                counter.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
                counter_grid.addWidget(counter,i,j, alignment=Qt.AlignLeft)
                self.stats[i * 2 + j] = counter

        for i in range(2):
            counter_grid.setColumnStretch(i, 1)
            counter_grid.setRowStretch(i, 1)

        bottom_layout.addLayout(counter_grid)

        #counter_grid.addStretch(1)
        bottom_layout.addStretch(1)
        self.final_counter = SimpleCounter("PUNTEGGIO:", self.textsize, self.textsize)
        bottom_layout.addWidget(self.final_counter)
        main_layout.addLayout(bottom_layout)

        self.setWindowTitle("Natura 2.5")
        self.setWindowIcon(QtGui.QIcon('data/nature.png'))
        self.twitchSignal.connect(self.twitchUpdate)

        self.setStyleSheet("background-color: black;  color:white;border: white;font-family:Pokemon GB")
        self.mainW = QWidget()
        self.mainW.setLayout(main_layout)
        self.setCentralWidget(self.mainW)


        if self.twitch:
            self.TwitchController = TwitchNaturaController.TwitchNaturaController(self.twitchSignal, self.config)
            self.TwitchController.start()

        if self.monitor:
            self.battleStats=[0]*4
            self.battleSwitch=False # last is in battle check
            self.gameSignal.connect(self.gameUpdate)
            self.gameMonitor = GameMonitorServer(self.gameSignal, self.config)
            self.gameMonitor.start()
    
    def updateNextMove(self,currlevel):

        # Find 4 moves closest to current level, going down
        closest_moves = []
        found_name=[]
        next_move=len(self.moves)
        search_next=True
        for lvl, move in reversed(self.moves):
            move_name = move[0]
            if lvl <= currlevel:
                if not move_name or move_name  in found_name:
                    continue
                closest_moves.append(move)
                found_name.append(move[0])
                if len(closest_moves) == 4:
                    break
                search_next=False
            elif search_next:
                next_move-=1
        closest_moves = list(reversed(closest_moves))
        while len(closest_moves) < 4:
            closest_moves.append(["","", 0, 0, 0, 0])
        for i in range(4):
            self.mv[i].updateMove(closest_moves[i])
        if next_move < len(self.moves):
            self.next.setText("Prossima: "+f"{self.moves[next_move][1][0]} ({self.moves[next_move][0]})")
        else: self.next.setText("Prossima: --")

    def closeEvent(self, a0: QCloseEvent) -> None:
        return super().closeEvent(a0)

    def quit(self):
        self.close()
        exit()

    def updateScore(self,levelUp=False,currLevel=0):
        if levelUp:
            self.monstats[5][1].setText(f"(X{round((2*self.lvlabel.get_count()+5)/(self.lvlabel.get_count()+5),2)})")
            self.updateNextMove(currLevel)
        if self.monitor:
            # ARROTONDA(MAX(0,001; 100 *    POTENZA(MAX(0; 1 - (C2 - 163000)/(1000000 - 163000)); 2) *    POTENZA(0,998; D2) *    POTENZA(0,7; E2) *    POTENZA(0,95; F2) *    POTENZA(0,8; G2) ); 3)
            # Translated to Python:
            # C2 = self.exp
            # D2 = self.stats[0].get_count()  # RESET
            # E2 = self.stats[2].get_count()  # SKIP
            # F2 = self.stats[1].get_count()  # EXTRA
            # G2 = self.stats[3].get_count()  # SELV.
            c2 = max(self.exp,163000)
            d2 = self.stats[0].get_count()
            e2 = self.stats[2].get_count()
            f2 = self.stats[1].get_count()
            g2 = self.stats[3].get_count()
            base = max(0, 1 - (c2 - 163000) / (self.maxexp - 163000))
            final_score = round(
                max(0.000,
                    100* (base ** 1.1)
                    * (0.998 ** d2)
                    * (0.7 ** e2)
                    * (0.95 ** f2)
                    * (0.8 ** g2)),2)
        else: final_score = max(
            0,
            10 - (max(0, self.lvlabel.get_count() - self.maxlevel) * 0.05 + self.stats[0].get_count() * 0.01 + self.stats[2].get_count() * 0.5 + self.stats[1].get_count() * 0.05 + self.stats[3].get_count() * 0.2)
        )
        self.final_counter.set_count(final_score)

    @pyqtSlot(int, int)
    def twitchUpdate(self, index, update):
        if index < 4:
            self.stats[index].set_count(update)
        else:
            self.lvlabel.set_count(update)
        self.updateScore(index==4,update)

    @pyqtSlot(str, str)
    def gameUpdate(self, datatype, data):
        values = [int(x, 16) for x in data.split("@")]
        if datatype != "GAMELOG":
            return
        #labels = ["LV", "PS", "VEL.", "ATT.", "SPEC.", "DIF.", "BATTLE", "BATTLEATT", "BATTLEDEF", "BATTLESPD","BATTLESPEC","EXP","HPEXP","ATTEXP","DEFEXP","SPDEXP","SPECEXP","PP1","PP2","PP3","PP4","MOVE","CURRPREC"]
       # for i, val in enumerate(values):
        #    print(f"{labels[i] if i < len(labels) else f'VAL{i}'}: {val}")
        
        
        values = data.split("@")
        try:
            lv = int(values[0],16)
            battle = int(values[6],16)
        except :
            print("exception in update from game")
            return
        if lv <3:
            return
        updateLV=False
        if not self.lvlabel.get_count()==lv: 
            self.lvlabel.set_count(lv)
            updateLV =True
            self.monstats[5][1].setText(f"(X{round((2*self.lvlabel.get_count()+5)/(self.lvlabel.get_count()+5),2)})")
            self.boostLabel.setText("Boost Stat. Esp. Massimo: +"+str(int(63*(self.lvlabel.get_count()/100))))
        for i in range(5):
            battlestat = int(values[i+6],16)#updated value
            actStat = int(values[i+1],16)
            statExp=int(values[i+12],16)
            statBoost= int((int(sqrt(statExp))*self.lvlabel.get_count())/400)
            self.monstats[i][1].setText("(+"+str(statBoost)+")")
            if statExp == 65535: #max stat exp
                self.monstats[i][1].setstyleSheet("color: lime")
            if i ==0 or battle==0 or battlestat==0: #PS, not in battle, 
                self.monstats[i][0].setText(str(actStat))
            else:
                    self.monstats[i][0].setText(str(battlestat))
                    if battlestat > actStat :
                        color = "lime"
                    elif battlestat < actStat:
                        color = "red"
                    else:
                        color = "white"
                    self.monstats[i][0].setStyleSheet(f"background-color: black; border:black; color:{color}")

        totExp = int(values[11],16)
        self.expLabel.setText("Exp: "+str(totExp))
        self.exp=totExp
        #17-20
        for i in range(0,4):
            self.mv[i].updatePP(int(values[i+17],16))
            if battle > 0:
                self.mv[i].updatePrec(int(values[21],16),int(values[22],16))
        self.updateScore(updateLV,lv)
        if (not self.battleSwitch) and battle >0: # not in battle but now we are
            self.battleSwitch=True
            return
        if self.battleSwitch and battle <1: # was in battle, now not anymore
            self.battleSwitch=False
            for i in range(4): #reset color
                self.monstats[i+1][0].setStyleSheet(f"background-color: black; border:black; color:white")
                self.mv[i].resetPrec()
        return
