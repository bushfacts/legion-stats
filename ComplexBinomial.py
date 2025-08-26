import pandas as pd
import math

data = [["BushFacts", True, 2, 3, 4, True, 5],
        ["BushFacts", False, 5, 0, 0, False, 0]]

def GetData():
    pass

# structure will be
# name, offense, red, black, white, surge, result
def CalculateProbabilities():
    for d in data:
        name = d[0]
        red = int(d[2])
        black = int(d[3])
        white = int(d[4])
        result = int(d[6])
        surge = 0
        if d[5]:
            surge = 1
        if d[1]:
            cumProb = 0
            for res in range(result, red + black + white + 1):
                cumProb = cumProb + OffenseSingleProb(red, black, white, surge, res)
        else:
            cumProb = 0
            for res in range(result, red + white + 1):
                cumProb = cumProb + DefenseSingleProb(red, white, surge, res)
            print(cumProb)
                
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

CalculateProbabilities()
