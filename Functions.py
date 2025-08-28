import pandas as pd
import csv

# parsing keywords I will be using:
# rolled,

def ScrapeChatLog(path, timeStart):
    data = []
    with open(path) as f:
        lines = f.readlines()
        parsing = False
        for i in range(0,len(lines)):
            if timeStart in lines[i]:
                parsing = True
            if parsing:
                if " rolled " in lines[i]:
                    data.append(ParseDieRoll(lines[i].strip(), lines[i+1].strip()))
    return data

def DFToCSV():
    pass

# can afford to be messy since this is computer generated text
# re-rolls currently ignored
def ParseDieRoll(line1, line2):
    timeStamp = line1.split("]")[0][1:]
    offense = False
    if " attack " in line1:
        offense = True
    blue = False
    if " RED " in line1:
        blue = True
    poolText = line1.split("(")[1][:-1].replace("pool:","").strip()
    pool = {"Red": 0, "Black": 0, "White": 0}
    poolText = poolText.split(" ")
    for p in poolText:
        if "R" in p:
            pool["Red"] = int(p.strip()[:-1])
        elif "B" in p:
            pool["Black"] = int(p.strip()[:-1])
        elif "W" in p:
            pool["White"] = int(p.strip()[:-1])

    results = {"Crits": 0, "Hits": 0, "Blocks": 0, "Surges": 0}
    line2 = line2.replace(".","")
    resultsText = line2.split(",")
    for r in resultsText:
        if "CRITS" in r:
            results["Crits"] = int(r.strip().split(" ")[0])
        elif "HITS" in r:
            results["Hits"] = int(r.strip().split(" ")[0])
        elif "BLOCKS" in r:
            results["Blocks"] = int(r.strip().split(" ")[0])
        elif "SURGES" in r:
            results["Surges"] = int(r.strip().split(" ")[0])

    data = {"Time": timeStamp, "Offense": offense, "Blue": blue, "Pool": pool, "Results": results}
    # print(data)
    return data
    

def ParseActions():
    pass

def ParseTimeStamp():
    pass
