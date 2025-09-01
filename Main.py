from Functions import *
from ComplexBinomial import *
import pathlib
import json

currentPath = pathlib.Path(__file__).parent.resolve()
timeStart = "[08:34:04]"

DATAPATH = currentPath.joinpath("Data\\Baer v BushFacts\\")
BLUE = "Brian Baer"
RED = "BushFacts"

RED_COLOR_PRIMARY = "salmon"
RED_COLOR_SECONDARY = "darkred"
BLUE_COLOR_PRIMARY = "steelblue"
BLUE_COLOR_SECONDARY = "darkblue"
BASE_COLOR = "lightgray"

# ScrapeChatLog(dataPath.joinPath("chat_log.txt"), timeStart)
# data = GetData(dataPath)


def ApplyProbabilities():
    attackData = []
    with open(DATAPATH.joinpath("attack_rolls.json"), "r") as file:
        attackData = json.load(file)
    for data in attackData:
        luckData = CalculateDiceProbability(data)
        if "Offense" in luckData:
            data["Offense"]["Probability"] = luckData["Offense"]
        if "Defense" in luckData:
            data["Defense"]["Probability"] = luckData["Defense"]
    with open(DATAPATH.joinpath("attack_rolls.json"), "w") as file:
        json.dump(attackData, file, indent=3)

