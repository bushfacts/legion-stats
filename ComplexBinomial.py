# probably want to emphasize how many dice are in each roll
# cover as a separate chart?
# totals to include: dice thrown, wounds delivered, blocks made, tokens gained (contrasted to total action breakdown)
# all actions taken: move, attack, aim, dodge, standby, guidance, force powers, etc 

import pandas as pd
import math
import pathlib
import json

def GetData(dataPath):
    with open(dataPath.joinpath("dice_rolls.json"),"r") as file:
        diceData = json.load(file) 
        return diceData

def CalculateAttackProbabilities(diceData):
    chartData = []
    for data in diceData:
        rd = data["Round"]
        attacker = data["Offense"]["Name"]
        red = data["Offense"]["Pool"]["Red"]
        black = data["Offense"]["Pool"]["Black"]
        white = data["Offense"]["Pool"]["White"]
        surge = data["Offense"]["Surge"]
        result = data["Offense"]["Result"]
        defender = data["Defense"]["Name"]
        dRed = data["Defense"]["Pool"]["Red"]
        dWhite = data["Defense"]["Pool"]["White"]
        dSurge = data["Defense"]["Surge"]
        dResult = data["Defense"]["Result"]

        cumOffenseProb = 0
        for res in range(result, red + black + white + 1):
            cumOffenseProb = cumOffenseProb + OffenseSingleProb(red, black, white, surge, res)

        cumDefenseProb = 0
        for dRes in range(dResult, dRed + dWhite + 1):
            cumDefenseProb = cumDefenseProb + DefenseSingleProb(dRed, dWhite, dSurge, dRes)
            
        chartData.append({"Round": rd,
                          "Attacker": {"Name": attacker, "P": max(1-cumOffenseProb,0), "Dice": red+black+white},
                          "Defender": {"Name": defender, "P": max(1-cumDefenseProb,0), "Dice": dRed+dWhite}
                          }) 

    return chartData
                
def OffenseSingleProb(red, black, white, surge, result):
    prob = 0
    integerPartitions = []
    for r in range(0, red + 1):
        for b in range(0, black + 1):
            for w in range(0, white + 1):
                if r + b + w == result:
                    integerPartitions.append([r,b,w])
    for [r,b,w] in integerPartitions:
        p = math.comb(red,r) * ((6+surge)/8)**(r) * ((2-surge)/8)**(red-r)
        p = p * math.comb(black,b) * ((4+surge)/8)**(b) * ((4-surge)/8)**(black-b)
        p = p * math.comb(white,w) * ((2+surge)/8)**(w) * ((6-surge)/8)**(white-w)
        prob = prob + p
    return prob

def DefenseSingleProb(red, white, surge, result):
    prob = 0
    integerPartitions = []
    for r in range(0, red + 1):
        for w in range(0, white + 1):
            if r + w == result:
                integerPartitions.append([r,w])
    for [r,w] in integerPartitions:
        p = math.comb(red,r) * ((3+surge)/6)**(r) * ((3-surge)/6)**(red-r)
        p = p * math.comb(white,w) * ((1+surge)/6)**(w) * ((5-surge)/6)**(white-w)
        prob = prob + p
    return prob

