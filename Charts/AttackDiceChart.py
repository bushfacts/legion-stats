# number of dice is a big skew factor here... can make the width of the bars = the sum of all dice rolled

#also, general note, get all the charts MADE, then worry about labeling and interactivity

# tooltips/info I want to see for this one:
# who is attacking who in each bar
# what round it is
# dice v dice and outcome
# Player names
# sorting might look cool

import plotly.graph_objects as go
import json
import pandas as pd
import numpy as np

import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import Main

attackData = []
with open(Main.DATAPATH.joinpath("attack_rolls.json"), "r") as file:
    attackData = json.load(file)

timeData = []
blueData = []
redData = []
diceCountData = []

timeIndex = 0
for data in attackData:
    timeIndex = timeIndex + 1
    timeData.append(timeIndex)
    if data["Offense"]["Name"] == Main.BLUE:
        blueData.append(data["Offense"]["Probability"])
        if "Defense" in data:
            redData.append(data["Defense"]["Probability"])
        else:
            redData.append(0)
    else:
        redData.append(data["Offense"]["Probability"])
        if "Defense" in data:
            blueData.append(data["Defense"]["Probability"])
        else:
            blueData.append(0)
    
    diceCount = data["Offense"]["Pool"]["Red"] + data["Offense"]["Pool"]["Black"] + data["Offense"]["Pool"]["White"]
    if "Defense" in data:
        diceCount = diceCount + data["Defense"]["Pool"]["Red"] + data["Defense"]["Pool"]["White"]
    diceCountData.append(diceCount)


df = pd.DataFrame({
    "time": timeData,
    "blue": blueData,
    "red": redData,
    "dice_count": diceCountData
})
df["base"] = df[["blue","red"]].min(axis=1)
df["blue_luck"] = (df["blue"]-df["red"]).clip(lower=0)
df["red_luck"] = (df["red"]-df["blue"]).clip(lower=0)
df["total_luck"] = df["red_luck"]+df["blue_luck"]+df["base"]

# df = df.sort_values("total_luck", ascending = False)

edges = [0] + [sum(df["dice_count"][:i+1]) for i in range(len(df["dice_count"]))]
centers = [(edges[i] + edges[i+1])/2 for i in range(len(df["dice_count"]))]

df = df.assign(center_point=centers)

fig = go.Figure()

fig.add_bar(
    x=df["center_point"], y=df["base"], width=df["dice_count"],
    name="Overlap", marker_color=Main.BASE_COLOR
)

fig.add_bar(
    x=df["center_point"], y=df["blue_luck"], width=df["dice_count"],
    name=Main.BLUE + " luck", marker_color=Main.BLUE_COLOR_PRIMARY
)

fig.add_bar(
    x=df["center_point"], y=df["red_luck"], width=df["dice_count"],
    name=Main.RED + " luck", marker_color=Main.RED_COLOR_PRIMARY
)

fig.update_layout(
    barmode = "stack",
    bargap=0, bargroupgap=0,
    title = "Attack Dice Luck Comparison",
    yaxis_title = "Luck",
    xaxis_title = "Total Dice Rolled"
)

fig.show()
fig.write_html(Main.DATAPATH.joinpath("Charts\\Attack Luck.html"))
