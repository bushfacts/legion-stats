import sys
import csv

from numpy import arange
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QCheckBox, QLabel, QLineEdit, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from Functions import *

offenseIndex = 0
defenseIndex = 0
mainIndex = 0

filePath = "chat_log.txt"
timeStart = "[08:34:04]"
diceData = ScrapeChatLog(filePath, timeStart)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dice Parse Helper")

        self.mainLayout = QGridLayout()

        font = "Baskerville"
        self.titleFont = QFont(font, 15)
        self.bodyFont = QFont(font, 10)

        self.spacer = QLabel()
        self.mainLayout.addWidget(self.spacer, 2, 0, 1, 2)

# 0-timestamp
# 1-attacker/defender
# 2-surge
# 3-red
# 4-black
# 5-white
# 6-result
# 7-buttons
# 8-submit
# 9-done

#region Labels
        self.redO = QLabel("Red")
        self.mainLayout.addWidget(self.redO, 3, 0, 1, 1, Qt.AlignmentFlag.AlignRight)
        self.blackO = QLabel("Black")
        self.mainLayout.addWidget(self.blackO, 4, 0, 1, 1, Qt.AlignmentFlag.AlignRight)
        self.whiteO = QLabel("White")
        self.mainLayout.addWidget(self.whiteO, 5, 0, 1, 1, Qt.AlignmentFlag.AlignRight)
        self.surgeO = QLabel("Surge")
        self.mainLayout.addWidget(self.surgeO, 2, 0, 1, 1, Qt.AlignmentFlag.AlignRight)
        self.redD = QLabel("Red")
        self.mainLayout.addWidget(self.redD, 3, 2, 1, 1, Qt.AlignmentFlag.AlignRight)
        self.whiteD = QLabel("White")
        self.mainLayout.addWidget(self.whiteD, 5, 2, 1, 1, Qt.AlignmentFlag.AlignRight)
        self.surgeD = QLabel("Surge")
        self.mainLayout.addWidget(self.surgeD, 2, 2, 1, 1, Qt.AlignmentFlag.AlignRight)
#endregion

#region information
        self.timeO = QLabel("fill")
        self.mainLayout.addWidget(self.timeO, 0, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        self.timeD = QLabel("fill")
        self.mainLayout.addWidget(self.timeD, 0, 2, 1, 2, Qt.AlignmentFlag.AlignCenter)

        self.nameO = QLabel("fill")
        self.mainLayout.addWidget(self.nameO, 1, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        self.nameD = QLabel("fill")
        self.mainLayout.addWidget(self.nameD, 1, 2, 1, 2, Qt.AlignmentFlag.AlignCenter)
#endregion

#region Inputs
        self.redOInput = QLineEdit()
        self.mainLayout.addWidget(self.redOInput, 3, 1, 1, 1)
        self.blackOInput = QLineEdit()
        self.mainLayout.addWidget(self.blackOInput, 4, 1, 1, 1)
        self.whiteOInput = QLineEdit()
        self.mainLayout.addWidget(self.whiteOInput, 5, 1, 1, 1)
        self.surgeOInput = QCheckBox()
        self.mainLayout.addWidget(self.surgeOInput, 2, 1, 1, 1)
        self.redDInput = QLineEdit()
        self.mainLayout.addWidget(self.redDInput, 3, 3, 1, 1)
        self.whiteDInput = QLineEdit()
        self.mainLayout.addWidget(self.whiteDInput, 5, 3, 1, 1)
        self.surgeDInput = QCheckBox()
        self.mainLayout.addWidget(self.surgeDInput, 2, 3, 1, 1)
#endregion

#region Buttons
        self.prevButtonL = QPushButton()
        self.prevButtonL.clicked.connect(PrevOffense)
        self.mainLayout.addWidget(self.prevButtonL, 7, 0, 1, 1)
        
        self.nextButtonL = QPushButton()
        self.nextButtonL.clicked.connect(NextOffense)
        self.mainLayout.addWidget(self.nextButtonL, 7, 1, 1, 1)
    
        self.prevButtonR = QPushButton()
        self.prevButtonR.clicked.connect(PrevDefense)
        self.mainLayout.addWidget(self.prevButtonR, 7, 2, 1, 1)
        
        self.nextButtonR = QPushButton()
        self.nextButtonR.clicked.connect(NextDefense)
        self.mainLayout.addWidget(self.nextButtonR, 7, 3, 1, 1)

        self.submitButton = QPushButton()
        self.submitButton.clicked.connect(Submit)
        self.mainLayout.addWidget(self.submitButton, 8, 0, 1, 4)

        self.doneButton = QPushButton()
        self.doneButton.clicked.connect(Done)
        self.mainLayout.addWidget(self.doneButton, 9, 0, 1, 4)
#endregion

        widget = QWidget()
        widget.setLayout(self.mainLayout)
        self.setCentralWidget(widget)

def NextOffense():
    offenseIndex = offenseIndex + 1

def PrevOffense():
    offenseIndex = offenseIndex - 1

def NextDefense():
    defenseIndex = defenseIndex + 1

def PrevDefense():
    defenseIndex = defenseIndex - 1

def Submit():
    NextOffense()
    NextDefense()

def Done():
    print(offenseIndex, defenseIndex)















app = QApplication(sys.argv)
window = MainWindow()
window.setMinimumSize(250,250)
window.show()
app.exec()
