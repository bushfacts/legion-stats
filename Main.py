from Functions import *
from ComplexBinomial import *
import pathlib
import json
import pandas as pd
import Data.Endless_v_MinorTom.MetaData as meta

currentPath = pathlib.Path(__file__).parent.resolve()
DATAPATH = currentPath.joinpath("Data\\Endless_v_MinorTom\\")

TIME_START = meta.TIME_START
BLUE = meta.BLUE
BLUE_UNITS = meta.BLUE_UNITS
BLUE_HEALTH = meta.BLUE_HEALTH
BLUE_EFF_HEALTH = meta.BLUE_EFF_HEALTH
BLUE_POINTS = meta.BLUE_POINTS
RED = meta.RED
RED_UNITS = meta.RED_UNITS
RED_HEALTH = meta.RED_HEALTH
RED_EFF_HEALTH = meta.RED_EFF_HEALTH
RED_POINTS = meta.RED_POINTS

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

def CombineDiceAndActions():
    attackData = []
    with open(DATAPATH.joinpath("attack_rolls.json"), "r") as file:
        attackData = json.load(file)
    actionDF = pd.read_csv(DATAPATH.joinpath("Actions.csv"))

    attackIndex = 0

    for index, activation in actionDF.iterrows():
        combined = {"Round": activation["Round"],
                    "Actions": [],
                    "Free Actions": [],
                    "Free Tokens": [],
                    "Unit": activation["Unit"],
                    "Player": activation["Player"],
                    "Target": [],
                    "Wounds": [],
                    "Notes": [],
                    "Attacks": []
                    }
        if not pd.isna(activation["Action 1"]): combined["Actions"].append(activation["Action 1"])
        if not pd.isna(activation["Action 2"]):
            if "//" in activation["Action 2"]:
                for x in activation["Action 2"].split("//"):
                    combined["Actions"].append(x)
            else:
                combined["Actions"].append(activation["Action 2"])
        if not pd.isna(activation["Free Actions"]): combined["Free Actions"].extend(activation["Free Actions"].split("//"))
        if not pd.isna(activation["Free Tokens"]): combined["Free Tokens"].extend(activation["Free Tokens"].split("//"))
        if not pd.isna(activation["Target"]): combined["Target"].extend(activation["Target"].split("//"))
        if not pd.isna(activation["Wounds"]): combined["Wounds"].extend(str(activation["Wounds"]).split("//"))
        if not pd.isna(activation["Notes"]): combined["Notes"].extend(activation["Notes"].split("//"))

        combined["Actions"] = [x.title() for x in combined["Actions"]]
        combined["Free Actions"] = [x.title() for x in combined["Free Actions"]]
        combined["Free Tokens"] = [x.title() for x in combined["Free Tokens"]]

        if ("Attack" in combined["Actions"] or "Attack" in combined["Free Actions"]):
            print("---------------")
            print(activation)
            for i in range(attackIndex, len(attackData)):
                print(attackData[i])
                userInput = input("?")
                if userInput == "y":
                    combined["Attacks"].append(attackData[i])
                    attackIndex = i
                    break
                else:
                    try:
                        int(userInput)
                        combined["Attacks"].append(attackData[i])
                        attackIndex = i
                    except ValueError:
                        pass
        with open(DATAPATH.joinpath("full_data.json"), "r") as file:
            fullData = json.load(file)
        with open(DATAPATH.joinpath("full_data.json"), "w") as file:
            fullData.append(combined)
            json.dump(fullData, file, indent=3)


    print(fullData)






# CheckFullData()
