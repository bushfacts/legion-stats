import pandas as pd
import math

data = [[True, 2, 3, 4, True, 5],
        [False, 5, 0, 0, False, 4]]

def GetData():
    pass

# structure will be
# offense, red, black, white, surge, result
def CalculateProbabilities():
    for d in data:
        red = int(d[1])
        black = int(d[2])
        white = int(d[3])
        result = int(d[5])
        surge = 0
        if d[4]:
            surge = 1
        if d[0]:
            cumProb = 0
            for res in range(result, red + black + white + 1):
                cumProb = cumProb + OffenseSingleProb(red, black, white, surge, res)
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

CalculateProbabilities()
