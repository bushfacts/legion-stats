import sys
import csv

from numpy import arange
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QCheckBox, QLabel, QLineEdit, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from Functions import *



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
widget = QWidget()
window = QMainWindow()
window.setCentralWidget(widget)
window.setWindowTitle("Dice Parse Helper")
window.setMinimumSize(250,250)

offenseIndex = 0
defenseIndex = 0
mainIndex = 0

filePath = "chat_log.txt"
timeStart = "[08:34:04]"
diceData = ScrapeChatLog(filePath, timeStart)

mainLayout = QGridLayout()
widget.setLayout(mainLayout)

font = "Baskerville"
titleFont = QFont(font, 15)
bodyFont = QFont(font, 10)

spacer = QLabel()
mainLayout.addWidget(spacer, 2, 0, 1, 2)

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
redO = QLabel("Red")    
mainLayout.addWidget(redO, 3, 0, 1, 1, Qt.AlignmentFlag.AlignRight)
blackO = QLabel("Black")
mainLayout.addWidget(blackO, 4, 0, 1, 1, Qt.AlignmentFlag.AlignRight)
whiteO = QLabel("White")
mainLayout.addWidget(whiteO, 5, 0, 1, 1, Qt.AlignmentFlag.AlignRight)
surgeO = QLabel("Surge")
mainLayout.addWidget(surgeO, 2, 0, 1, 1, Qt.AlignmentFlag.AlignRight)
redD = QLabel("Red")
mainLayout.addWidget(redD, 3, 2, 1, 1, Qt.AlignmentFlag.AlignRight)
whiteD = QLabel("White")
mainLayout.addWidget(whiteD, 5, 2, 1, 1, Qt.AlignmentFlag.AlignRight)
surgeD = QLabel("Surge")
mainLayout.addWidget(surgeD, 2, 2, 1, 1, Qt.AlignmentFlag.AlignRight)
#endregion

#region information
timeO = QLabel("fill")
mainLayout.addWidget(timeO, 0, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
timeD = QLabel("fill")
mainLayout.addWidget(timeD, 0, 2, 1, 2, Qt.AlignmentFlag.AlignCenter)

nameO = QLabel("fill")
mainLayout.addWidget(nameO, 1, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
nameD = QLabel("fill")
mainLayout.addWidget(nameD, 1, 2, 1, 2, Qt.AlignmentFlag.AlignCenter)
#endregion

#region Inputs
redOInput = QLineEdit()
mainLayout.addWidget(redOInput, 3, 1, 1, 1)
blackOInput = QLineEdit()
mainLayout.addWidget(blackOInput, 4, 1, 1, 1)
whiteOInput = QLineEdit()
mainLayout.addWidget(whiteOInput, 5, 1, 1, 1)
surgeOInput = QCheckBox()
mainLayout.addWidget(surgeOInput, 2, 1, 1, 1)
redDInput = QLineEdit()
mainLayout.addWidget(redDInput, 3, 3, 1, 1)
whiteDInput = QLineEdit()
mainLayout.addWidget(whiteDInput, 5, 3, 1, 1)
surgeDInput = QCheckBox()
mainLayout.addWidget(surgeDInput, 2, 3, 1, 1)
#endregion

#region Buttons
prevButtonL = QPushButton()
prevButtonL.clicked.connect(PrevOffense)
mainLayout.addWidget(prevButtonL, 7, 0, 1, 1)

nextButtonL = QPushButton()
nextButtonL.clicked.connect(NextOffense)
mainLayout.addWidget(nextButtonL, 7, 1, 1, 1)

prevButtonR = QPushButton()
prevButtonR.clicked.connect(PrevDefense)
mainLayout.addWidget(prevButtonR, 7, 2, 1, 1)

nextButtonR = QPushButton()
nextButtonR.clicked.connect(NextDefense)
mainLayout.addWidget(nextButtonR, 7, 3, 1, 1)

submitButton = QPushButton()
submitButton.clicked.connect(Submit)
mainLayout.addWidget(submitButton, 8, 0, 1, 4)

doneButton = QPushButton()
doneButton.clicked.connect(Done)
mainLayout.addWidget(doneButton, 9, 0, 1, 4)
#endregion

window.show()
app.exec()
