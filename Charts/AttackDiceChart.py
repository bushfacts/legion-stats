# add vertical line separating each round

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

fullData = []
with open(Main.DATAPATH.joinpath("full_data.json"), "r") as file:
    fullData = json.load(file)

timeData = []
blueData = []
redData = []
diceCountData = []
round = []
activationCounts = []
attacker = []
attackingUnit = []
attackDice = []
attackHits = []
defender = []
defendingUnit = []
defenseDice = []
defenseBlocks = []
wounds = []

timeIndex = 0
activationNumber = 1
for activation in fullData:
    targetNumber = 0
    if len(round) > 0:
        if not round[-1] == activation["Round"]: activationNumber = 1        
    for data in activation["Attacks"]:
        timeData.append(timeIndex)
        round.append(activation["Round"])
        activationCounts.append(activationNumber)
        attacker.append(data["Offense"]["Name"])
        attackingUnit.append(activation["Unit"])
        attackDice.append(data["Offense"]["Pool"]["Red"]+data["Offense"]["Pool"]["Black"]+data["Offense"]["Pool"]["White"])
        attackHits.append(data["Offense"]["Result"])
        if data["Offense"]["Name"] == Main.BLUE:
            defender.append(Main.RED)
        else:
            defender.append(Main.BLUE)
        if "Defense" in data:
            defenseDice.append(data["Defense"]["Pool"]["Red"]+data["Defense"]["Pool"]["White"])
            defenseBlocks.append(data["Defense"]["Result"])
        else:
            defenseDice.append(0)
            defenseBlocks.append(0)
        defendingUnit.append(activation["Target"][targetNumber])
        wounds.append(int(float(activation["Wounds"][targetNumber])))
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

        targetNumber = targetNumber + 1
        timeIndex = timeIndex + 1
    activationNumber = activationNumber + 1



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
df["blue_probability"] = 1 - df["blue"]
df["red_probability"] = 1 - df["red"]
df["attacking_unit"] = attackingUnit
df["defending_unit"] = defendingUnit
df["attacker"] = attacker
df["defender"] = defender
df["round"] = round
df["activation_number"] = activationCounts
df["wounds"] = wounds
df["attack_dice"] = attackDice
df["attack_hits"] = attackHits
df["defense_dice"] = defenseDice
df["defense_blocks"] = defenseBlocks

blueSortWeights = []
for index, row in df.iterrows():
    if row["blue"] > row["red"]:
        blueSortWeights.append(row["blue"])
    else:
        blueSortWeights.append(-1 * row["red"])

df["blue_sort_weights"] = blueSortWeights
sortedDF = df.sort_values("blue_sort_weights", ascending=False)

fig = go.Figure()

#region traces for unsorted view
edges = [0] + [sum(df["dice_count"][:i+1]) for i in range(len(df["dice_count"]))]
centers = [(edges[i] + edges[i+1])/2 for i in range(len(df["dice_count"]))]
df = df.assign(center_point=centers)

hoverDataDF = df[["blue_probability", "red_probability", "attacking_unit", "defending_unit",
                   "attacker", "defender", "round", "activation_number", "wounds",
                   "attack_dice", "attack_hits", "defense_dice", "defense_blocks"]]

fig.add_bar(
    x=df["center_point"], y=df["base"], width=df["dice_count"],
    name="Overlap", marker_color=Main.BASE_COLOR,
    customdata=hoverDataDF
)

fig.add_bar(
    x=df["center_point"], y=df["blue_luck"], width=df["dice_count"],
    name=Main.BLUE + " luckier", marker_color=Main.BLUE_COLOR_PRIMARY,
    customdata=hoverDataDF
)

fig.add_bar(
    x=df["center_point"], y=df["red_luck"], width=df["dice_count"],
    name=Main.RED + " luckier", marker_color=Main.RED_COLOR_PRIMARY,
    customdata=hoverDataDF
)
#endregion

#region add traces for sorted view
sortedEdges = [0] + [sum(sortedDF["dice_count"][:i+1]) for i in range(len(sortedDF["dice_count"]))]
sortedCenters = [(sortedEdges[i] + sortedEdges[i+1])/2 for i in range(len(sortedDF["dice_count"]))]
sortedDF = sortedDF.assign(center_point=sortedCenters)

sortedHoverDataDF = sortedDF[["blue_probability", "red_probability", "attacking_unit", "defending_unit",
                   "attacker", "defender", "round", "activation_number", "wounds",
                   "attack_dice", "attack_hits", "defense_dice", "defense_blocks"]]

fig.add_bar(
    x=sortedDF["center_point"], y=sortedDF["base"], width=sortedDF["dice_count"],
    name="Overlap", marker_color=Main.BASE_COLOR,
    visible=False, customdata=sortedHoverDataDF
)

fig.add_bar(
    x=sortedDF["center_point"], y=sortedDF["blue_luck"], width=sortedDF["dice_count"],
    name=Main.BLUE + " luckier", marker_color=Main.BLUE_COLOR_PRIMARY,
    visible=False, customdata=sortedHoverDataDF
)

fig.add_bar(
    x=sortedDF["center_point"], y=sortedDF["red_luck"], width=sortedDF["dice_count"],
    name=Main.RED + " luckier", marker_color=Main.RED_COLOR_PRIMARY,
    visible=False, customdata=sortedHoverDataDF
)
#endregion

fig.update_layout(
    barmode = "stack",
    bargap=0, bargroupgap=0,
    title = "Attack Dice Luck Comparison",
    yaxis_title = "Luck",
    xaxis_title = "Total Dice Rolled",
    updatemenus=[
        dict(
            type="buttons",
            direction="right",
            active=1,
            x=0.57,
            y=1.2,
            buttons=list([
                dict(label="Time",
                        method="update",
                        args=[{"visible": [True, True, True, False, False, False]},
                            {"title": "Time"}]),
                dict(label="Sorted",
                        method="update",
                        args=[{"visible": [False, False, False, True, True, True]},
                            {"title": "Sorted"}]),
            ]),
        )
    ]
)

fig.update_traces(
    hovertemplate = "<br>".join([
        "Round: %{customdata[6]}",
        "Activation: %{customdata[7]}",
        "",
        "Attacker: %{customdata[4]}",
        "%{customdata[2]}",
        "%{customdata[10]} out of %{customdata[9]} hit(s)",
        "",
        "Defender: %{customdata[5]}",
        "%{customdata[3]}",
        "%{customdata[12]} out of %{customdata[11]} block(s)",
        "",
        "Blue Probability: %{customdata[0]:,.0%}",
        "Red Probability: %{customdata[1]:,.0%}",
        "",
        "Wounds Dealt: %{customdata[8]}",
        "</br><extra></extra>"
    ])
)

fig.show()

fig.write_html(Main.DATAPATH.joinpath("Charts\\Attack Luck.html"))
