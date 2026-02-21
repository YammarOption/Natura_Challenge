
from configparser import ConfigParser
from PyQt5.QtWidgets import (QApplication, QErrorMessage)
from src.GUI.NaturaMainWindow import NaturaMainWindow
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QListWidget, QPushButton
from PyQt5 import QtGui

class ListSelectorDialog(QDialog):
    def __init__(self, items, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Seleziona Pokémon")
        self.selected_item = None
        self.setWindowIcon(QtGui.QIcon('data/nature.png'))
        layout = QVBoxLayout(self)
        self.list_widget = QListWidget(self)
        self.list_widget.addItems(items)
        layout.addWidget(self.list_widget)

        select_button = QPushButton("Vai", self)
        select_button.clicked.connect(self.select_item)
        layout.addWidget(select_button)

    def select_item(self):
        selected = self.list_widget.currentItem()
        if selected:
            self.selected_item = selected.text()
            self.accept()


if not __name__ == "__main__":
    exit()
app = QApplication([])
config = ConfigParser()
config.read("Config.ini")
gen1_pokemon = [
    "Bulbasaur", "Ivysaur", "Venusaur",
    "Charmander", "Charmeleon", "Charizard",
    "Squirtle", "Wartortle", "Blastoise",
    "Caterpie", "Metapod", "Butterfree",
    "Weedle", "Kakuna", "Beedrill",
    "Pidgey", "Pidgeotto", "Pidgeot",
    "Rattata", "Raticate",
    "Spearow", "Fearow",
    "Ekans", "Arbok",
    "Pikachu", "Raichu",
    "Sandshrew", "Sandslash",
    "Nidoranf", "Nidorina", "Nidoqueen",
    "Nidoranm", "Nidorino", "Nidoking",
    "Clefairy", "Clefable",
    "Vulpix", "Ninetales",
    "Jigglypuff", "Wigglytuff",
    "Zubat", "Golbat",
    "Oddish", "Gloom", "Vileplume",
    "Paras", "Parasect",
    "Venonat", "Venomoth",
    "Diglett", "Dugtrio",
    "Meowth", "Persian",
    "Psyduck", "Golduck",
    "Mankey", "Primeape",
    "Growlithe", "Arcanine",
    "Poliwag", "Poliwhirl", "Poliwrath",
    "Abra", "Kadabra", "Alakazam",
    "Machop", "Machoke", "Machamp",
    "Bellsprout", "Weepinbell", "Victreebel",
    "Tentacool", "Tentacruel",
    "Geodude", "Graveler", "Golem",
    "Ponyta", "Rapidash",
    "Slowpoke", "Slowbro",
    "Magnemite", "Magneton",
    "Farfetchd",
    "Doduo", "Dodrio",
    "Seel", "Dewgong",
    "Grimer", "Muk",
    "Shellder", "Cloyster",
    "Gastly", "Haunter", "Gengar",
    "Onix",
    "Drowzee", "Hypno",
    "Krabby", "Kingler",
    "Voltorb", "Electrode",
    "Exeggcute", "Exeggutor",
    "Cubone", "Marowak",
    "Hitmonlee", "Hitmonchan",
    "Lickitung",
    "Koffing", "Weezing",
    "Rhyhorn", "Rhydon",
    "Chansey",
    "Tangela",
    "Kangaskhan",
    "Horsea", "Seadra",
    "Goldeen", "Seaking",
    "Staryu", "Starmie",
    "MrMime",
    "Scyther",
    "Jynx",
    "Electabuzz",
    "Magmar",
    "Pinsir",
    "Tauros",
    "Magikarp", "Gyarados",
    "Lapras",
    "Ditto",
    "Eevee", "Vaporeon", "Jolteon", "Flareon",
    "Porygon",
    "Omanyte", "Omastar",
    "Kabuto", "Kabutops",
    "Aerodactyl",
    "Snorlax",
    "Articuno", "Zapdos", "Moltres",
    "Dratini", "Dragonair", "Dragonite",
    "Mewtwo", "Mew","Missingno"
]

dialog = ListSelectorDialog(gen1_pokemon)
if dialog.exec_() == QDialog.Accepted:
    selected_value = dialog.selected_item
else:
    exit()
try:
    window = NaturaMainWindow(selected_value.lower(),config,"3.0")
except:
    exit()
if not  window:
    error = QErrorMessage()
    error.showMessage("Errore")
    app.exec()
    exit()
window.setup(config)
window.show()
app.exec()
