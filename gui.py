import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys, requests
from main import Api

lcu = Api()

class window(QWidget):
    lcu.setChampion('Riven')

    def __init__(self, parent=None):

        super(window, self).__init__(parent)
        self.resize(500, 500)
        self.setWindowTitle('Liga legend')
        self.mainImage = QLabel(self)
        self.labelQ = QLabel(self)
        self.labelQ.move(100, 0)
        self.labelW = QLabel(self)
        self.labelW.move(200, 0)
        self.labelE = QLabel(self)
        self.labelE.move(300, 0)
        self.labelR = QLabel(self)
        self.labelR.move(400, 0)
        self.images()

    def images(self):
        spells = lcu.getSpellsImage()
        image = requests.get(lcu.getChampionImage())
        self.champImage = QPixmap()
        self.champImage.loadFromData(image.content)
        self.mainImage.setPixmap(self.champImage)

        #Spell Q
        image = requests.get(spells[0])
        self.Q = QPixmap()
        self.Q.loadFromData(image.content)
        self.labelQ.setPixmap(self.Q)

        #Spell W
        image = requests.get(spells[1])
        self.W = QPixmap()
        self.W.loadFromData(image.content)
        self.labelW.setPixmap(self.W)

        #Spell E
        image = requests.get(spells[2])
        self.E = QPixmap()
        self.E.loadFromData(image.content)
        self.labelE.setPixmap(self.W)

        #Spell R
        image = requests.get(spells[3])
        self.R = QPixmap()
        self.R.loadFromData(image.content)
        self.labelR.setPixmap(self.R)
        
        
def main():
    app = QApplication(sys.argv)
    ex = window()
    ex.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()