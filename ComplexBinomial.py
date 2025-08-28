# probably want to emphasize how many dice are in each roll
# cover as a separate chart?
# totals to include: dice thrown, wounds delivered, blocks made, tokens gained (contrasted to total action breakdown)
# all actions taken: move, attack, aim, dodge, standby, guidance, force powers, etc 

import pandas as pd
import math


def GetData():
    df = pd.read_csv("test data.csv")
    return df

def CalculateAttackProbabilities(data):
    chartData = []
    for d in data.iterrows():
        rd = d[1]["Round"]
        attacker = d[1]["Attacker"]
        red = int(d[1]["Red"])
        black = int(d[1]["Black"])
        white = int(d[1]["White"])
        surge = d[1]["Surge"]
        result = int(d[1]["Result"])
        defender = d[1]["Defender"]
        dRed = int(d[1]["dRed"])
        dWhite = int(d[1]["dWhite"])
        dSurge = d[1]["dSurge"]
        dResult = int(d[1]["dResult"])

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

data = GetData()
luckData = CalculateAttackProbabilities(data)
print(luckData)
