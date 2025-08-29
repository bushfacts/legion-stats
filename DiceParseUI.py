import sys
import csv

from numpy import arange
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QCheckBox, QLabel, QLineEdit, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import pathlib
import json

from Functions import *

currentPath = pathlib.Path(__file__).parent.resolve()
dataPath = currentPath.joinpath("Data\\Baer v BushFacts\\")
timeStart = "[08:34:04]"

BLUEPLAYER = "Brian Baer"
REDPLAYER = "BushFacts"

##################################################
# FUNCTIONS
##################################################

# these Get functions are inefficient by choice for robustitudeness
#region Offense Functions
def NextOffense():
    global offenseIndex
    offenseIndex = offenseIndex + 1
    dieRoll = GetOffense()
    UpdateOffense(dieRoll)

def PrevOffense():
    global offenseIndex
    offenseIndex = offenseIndex - 1
    dieRoll = GetOffense()
    UpdateOffense(dieRoll)

def GetOffense():
    global offenseIndex
    global diceData
    count = 0
    for i in range(0,len(diceData)):
        if diceData[i]["Offense"]:
            if count == offenseIndex:
                print(diceData[i])
                return diceData[i]
            count = count + 1

def UpdateOffense(dieRoll):
    global timeO
    global nameO
    global redOInput
    global blackOInput
    global whiteOInput
    global offenseDictResult
    timeO.setText(dieRoll['Time'])
    nameO.setText(BLUEPLAYER if dieRoll['Blue'] else REDPLAYER)
    redOInput.setText(str(dieRoll['Pool']['Red']))
    blackOInput.setText(str(dieRoll['Pool']['Black']))
    whiteOInput.setText(str(dieRoll['Pool']['White']))
    offenseDictResult = dieRoll['Results']
    UpdateOffenseResults()

def UpdateOffenseResults():
    global surgeOInput
    global resultOInput
    global offenseDictResult
    if surgeOInput.isChecked():
        resultOInput.setText(str(offenseDictResult['Crits'] + offenseDictResult['Hits'] + offenseDictResult['Surges']))
    else:
        resultOInput.setText(str(offenseDictResult['Crits'] + offenseDictResult['Hits']))
#endregion

#region Defense Functions
def NextDefense():
    global defenseIndex
    defenseIndex = defenseIndex + 1
    dieRoll = GetDefense()
    UpdateDefense(dieRoll)

def PrevDefense():
    global defenseIndex
    defenseIndex = defenseIndex - 1
    dieRoll = GetDefense()
    UpdateDefense(dieRoll)

def GetDefense():
    global defenseIndex
    global diceData
    count = 0
    for i in range(0,len(diceData)):
        if not diceData[i]["Offense"]:
            if count == defenseIndex:
                print(diceData[i])
                return diceData[i]
            count = count + 1

def UpdateDefense(dieRoll):
    global timeD
    global nameD
    global redDInput
    global whiteDInput
    global defenseDictResult
    timeD.setText(dieRoll['Time'])
    nameD.setText(BLUEPLAYER if dieRoll['Blue'] else REDPLAYER)
    redDInput.setText(str(dieRoll['Pool']['Red']))
    whiteDInput.setText(str(dieRoll['Pool']['White']))
    defenseDictResult = dieRoll['Results']
    UpdateDefenseResults()
    
def UpdateDefenseResults():
    global surgeDInput
    global resultDInput
    global defenseDictResult
    if surgeDInput.isChecked():
        resultDInput.setText(str(defenseDictResult['Blocks'] + defenseDictResult['Surges']))
    else:
        resultDInput.setText(str(defenseDictResult['Blocks']))
#endregion

def NextSyncd():
    global offenseIndex
    global defenseIndex
    global diceData

    offenseIndex = offenseIndex + 1
    count = 0
    offenseDieRoll = {}
    defenseDieRoll = {}
    offenseFound = False
    for i in range(0,len(diceData)):
        if diceData[i]["Offense"]:
            if count == offenseIndex:
                offenseDieRoll = diceData[i]
                offenseFound = True
            else:
                count = count + 1
        elif offenseFound:
            defenseDieRoll = diceData[i]
            break

    UpdateOffense(offenseDieRoll)
    UpdateDefense(defenseDieRoll)

def Rally():
    pass

def Cover():
    pass

def Submit():
    global roundInput
    global timeO
    global timeD
    global nameO
    global nameD
    global surgeOInput
    global surgeDInput
    global redOInput
    global blackOInput
    global whiteOInput
    global redDInput
    global whiteDInput
    global resultOInput
    global resultDInput
    thisResult = {
        "Round": int(roundInput.text()),
        "Offense": {
            "Time": timeO.text(),
            "Name": nameO.text(),
            "Surge": surgeOInput.isChecked(),
            "Pool": {"Red": int(redOInput.text()), "Black": int(blackOInput.text()), "White": int(whiteOInput.text())},
            "Result": int(resultOInput.text()),
            "Probability": 0
        },
        "Defense": {
            "Time": timeD.text(),
            "Name": nameD.text(),
            "Surge": surgeDInput.isChecked(),
            "Pool": {"Red": int(redDInput.text()), "White": int(whiteDInput.text())},
            "Result": int(resultDInput.text()),
            "Probability": 0
        }
    }
    print(thisResult)
    allResults = []
    with open(dataPath.joinpath("dice_rolls.json"), "r") as file:
        allResults = json.load(file)
        # allResults.append(thisResult)
        # json.dump(allResults, file, indent=3)
    with open(dataPath.joinpath("dice_rolls.json"), "w") as file:
        # allResults = json.load(file)
        allResults.append(thisResult)
        json.dump(allResults, file, indent=3)

    NextSyncd()

def Done():
    global offenseIndex
    global defenseIndex
    print(offenseIndex, defenseIndex)



##################################################
# GUI
##################################################

app = QApplication(sys.argv)
widget = QWidget()
window = QMainWindow()
window.setCentralWidget(widget)
window.setWindowTitle("Dice Parse Helper")
window.setMinimumSize(250,250)

offenseIndex = 0
offenseDictResult = {}
defenseIndex = 0
defenseDictResult = {}
mainIndex = 0
fullResults = []

diceData = ScrapeChatLog(dataPath.joinpath("chat_log.txt"), timeStart)

mainLayout = QGridLayout()
widget.setLayout(mainLayout)

font = "Baskerville"
titleFont = QFont(font, 15)
bodyFont = QFont(font, 10)

spacer = QLabel()
mainLayout.addWidget(spacer, 2, 0, 1, 2)

# 0-round 
# 1-timestamp
# 2-attacker/defender
# 3-surge
# 4-red
# 5-black
# 6-white
# 7-result
# 8-buttons
# 9-submit
# 10-done

#region Labels
redO = QLabel("Red")    
mainLayout.addWidget(redO, 4, 0, 1, 1, Qt.AlignmentFlag.AlignRight)
blackO = QLabel("Black")
mainLayout.addWidget(blackO, 5, 0, 1, 1, Qt.AlignmentFlag.AlignRight)
whiteO = QLabel("White")
mainLayout.addWidget(whiteO, 6, 0, 1, 1, Qt.AlignmentFlag.AlignRight)
resultO = QLabel("Result")
mainLayout.addWidget(resultO, 7, 0, 1, 1, Qt.AlignmentFlag.AlignRight)
surgeO = QLabel("Surge")
mainLayout.addWidget(surgeO, 3, 0, 1, 1, Qt.AlignmentFlag.AlignRight)
redD = QLabel("Red")
mainLayout.addWidget(redD, 4, 2, 1, 1, Qt.AlignmentFlag.AlignRight)
whiteD = QLabel("White")
mainLayout.addWidget(whiteD, 6, 2, 1, 1, Qt.AlignmentFlag.AlignRight)
resultD = QLabel("Result")
mainLayout.addWidget(resultD, 7, 2, 1, 1, Qt.AlignmentFlag.AlignRight)
surgeD = QLabel("Surge")
mainLayout.addWidget(surgeD, 3, 2, 1, 1, Qt.AlignmentFlag.AlignRight)
round = QLabel("Round")
mainLayout.addWidget(round, 0, 0, 1, 2, Qt.AlignmentFlag.AlignRight)
#endregion

#region information
timeO = QLabel("fill")
mainLayout.addWidget(timeO, 1, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
timeD = QLabel("fill")
mainLayout.addWidget(timeD, 1, 2, 1, 2, Qt.AlignmentFlag.AlignCenter)
nameO = QLabel("fill")
mainLayout.addWidget(nameO, 2, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
nameD = QLabel("fill")
mainLayout.addWidget(nameD, 2, 2, 1, 2, Qt.AlignmentFlag.AlignCenter)
#endregion

#region Inputs
redOInput = QLineEdit()
mainLayout.addWidget(redOInput, 4, 1, 1, 1)
blackOInput = QLineEdit()
mainLayout.addWidget(blackOInput, 5, 1, 1, 1)
whiteOInput = QLineEdit()
mainLayout.addWidget(whiteOInput, 6, 1, 1, 1)
resultOInput = QLineEdit()
mainLayout.addWidget(resultOInput, 7, 1, 1, 1)
surgeOInput = QCheckBox()
surgeOInput.stateChanged.connect(UpdateOffenseResults)
mainLayout.addWidget(surgeOInput, 3, 1, 1, 1)
redDInput = QLineEdit()
mainLayout.addWidget(redDInput, 4, 3, 1, 1)
whiteDInput = QLineEdit()
mainLayout.addWidget(whiteDInput, 6, 3, 1, 1)
resultDInput = QLineEdit()
mainLayout.addWidget(resultDInput, 7, 3, 1, 1)
surgeDInput = QCheckBox()
surgeDInput.stateChanged.connect(UpdateDefenseResults)
mainLayout.addWidget(surgeDInput, 3, 3, 1, 1)
roundInput = QLineEdit()
mainLayout.addWidget(roundInput, 0, 2, 1, 1)
#endregion

#region Buttons
prevButtonL = QPushButton("Prev")
prevButtonL.clicked.connect(PrevOffense)
mainLayout.addWidget(prevButtonL, 8, 0, 1, 1)

nextButtonSyncd = QPushButton("Next (sync'd)")
nextButtonSyncd.clicked.connect(NextSyncd)
mainLayout.addWidget(nextButtonSyncd, 8, 1, 1, 1)

nextButtonL = QPushButton("Next")
nextButtonL.clicked.connect(NextOffense)
mainLayout.addWidget(nextButtonL, 9, 1, 1, 1)

prevButtonR = QPushButton("Prev")
prevButtonR.clicked.connect(PrevDefense)
mainLayout.addWidget(prevButtonR, 8, 2, 1, 1)

nextButtonR = QPushButton("Next")
nextButtonR.clicked.connect(NextDefense)
mainLayout.addWidget(nextButtonR, 8, 3, 1, 1)

rallyButton = QPushButton("Submit as Rally")
rallyButton.clicked.connect(Rally)
mainLayout.addWidget(rallyButton, 9, 2, 1, 1)

coverButton = QPushButton("Submit as Cover")
coverButton.clicked.connect(Cover)
mainLayout.addWidget(coverButton, 9, 3, 1, 1)

submitButton = QPushButton("Submit")
submitButton.clicked.connect(Submit)
mainLayout.addWidget(submitButton, 10, 0, 1, 4)

doneButton = QPushButton("Done")
doneButton.clicked.connect(Done)
mainLayout.addWidget(doneButton, 11, 0, 1, 4)
#endregion

for i in range(0,mainLayout.columnCount()):
    mainLayout.setColumnStretch(i, 1)

window.show()
app.exec()
