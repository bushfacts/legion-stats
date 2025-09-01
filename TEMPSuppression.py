import Main
import sys
import json
from Functions import *
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QScrollArea, QLabel, QPushButton, QCheckBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

#gonna rely on unique time stamps in the chat log

diceData = ScrapeDice()

def CreateDiceRollWidget(data):
    widgets = []

    widgets.append(QLabel(data["Time"]))
    if data["Offense"]:
        widgets.append(QLabel("Offense"))
    else:
        widgets.append(QLabel("Defense"))

    if data["Blue"]:
        widgets.append(QLabel(Main.BLUE))
    else:
        widgets.append(QLabel(Main.RED))

    widgets.append(QLabel(str(data["Pool"]["Red"])))
    widgets.append(QLabel(str(data["Pool"]["Black"])))
    widgets.append(QLabel(str(data["Pool"]["White"])))
    widgets.append(QLabel(str(data["Results"]["Blocks"] + data["Results"]["Surges"])))

    if not data["Offense"]:
        widgets.append(QCheckBox())
        
    return widgets

def SubmitButton():
    global diceWidgets
    suppresionData = []
    for diceRow in diceWidgets:
        if len(diceRow) == 8:
            if diceRow[7].isChecked():
                thisData = {"Time": diceRow[0].text(),
                            "Player": diceRow[2].text(),
                            "Roll": str(int(diceRow[3].text()) + int(diceRow[5].text())),
                            "Result": diceRow[6].text()}
                suppresionData.append(thisData)
                print(diceRow[0].text())

    with open(Main.DATAPATH.joinpath("suppression.json"), "w") as file:
        json.dump(suppresionData, file, indent=3)
    

#######################################################
# GUI
#######################################################

app = QApplication(sys.argv)
centralWidget = QWidget()
window = QMainWindow()
window.setCentralWidget(centralWidget)
window.setWindowTitle("Suppression Helper")
window.setMinimumSize(320,720)

diceData = ScrapeDice()
diceWidgets = []

mainLayout = QGridLayout()
centralWidget.setLayout(mainLayout)

scrollArea = QScrollArea(centralWidget)
scrollArea.setGeometry(10, 10, 300, 600)
scrollArea.setWidgetResizable(True)
container = QWidget()
scrollArea.setWidget(container)

vLayout = QVBoxLayout(container)
vLayout.setContentsMargins(10, 10, 10, 10)

i = 0
for dice in diceData:
    widgets = CreateDiceRollWidget(dice)
    hLayout = QHBoxLayout()
    thisRow = []
    for j in range(0, len(widgets)):
        thisRow.append(widgets[j])
        hLayout.addWidget(widgets[j])
    diceWidgets.append(thisRow)
    i = i + 1
    hLayout.addStretch()
    vLayout.addLayout(hLayout)

submitButton = QPushButton("Submit")
submitButton.clicked.connect(SubmitButton)
mainLayout.addWidget(submitButton, 0,0, Qt.AlignmentFlag.AlignBottom)

window.show()
app.exec()
