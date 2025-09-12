import plotly.graph_objects as go
import pandas as pd
import json
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import Main

df = pd.read_csv(Main.DATAPATH.joinpath("Actions.csv"))

ACTIONS = ["Aim", "Dodge", "Move", "Standby", "Attack", "Recover", "Force Push", "Force Choke", "Quick Thinking"]
MOVES = ["Withdraw", "Move", "Climb", "Scout"]

fullData = []
with open(Main.DATAPATH.joinpath("full_data.json"), "r") as file:
    fullData = json.load(file)

actionCounts = {"Red": [0 for x in ACTIONS],
                "Blue": [0 for x in ACTIONS]}
freeActionCounts = {"Red": [0 for x in ACTIONS],
                    "Blue": [0 for x in ACTIONS]}

for activation in fullData:
    player = activation["Player"].title()
    for action in activation["Actions"]:
        if action in MOVES:
            actionCounts[player][ACTIONS.index("Move")] = actionCounts[player][ACTIONS.index("Move")] + 1
        else:
            actionCounts[player][ACTIONS.index(action)] = actionCounts[player][ACTIONS.index(action)] + 1
    for action in activation["Free Actions"]:
        freeActionCounts[player][ACTIONS.index(action)] = freeActionCounts[player][ACTIONS.index(action)] + 1


actionsDF = pd.DataFrame({
    "red_actions": actionCounts["Red"],
    "blue_actions": actionCounts["Blue"],
    "red_free_actions": freeActionCounts["Red"],
    "blue_free_actions": freeActionCounts["Blue"],
    "red_all_actions": [actionCounts["Red"][i] + freeActionCounts["Red"][i] for i in range(len(ACTIONS))],
    "blue_all_actions": [actionCounts["Blue"][i] + freeActionCounts["Blue"][i] for i in range(len(ACTIONS))]
})

fig = go.Figure()

fig.add_bar(
    x=ACTIONS, y=actionsDF["blue_all_actions"],
    name=Main.BLUE, marker_color=Main.BLUE_COLOR_PRIMARY,
    visible=False
)

fig.add_bar(
    x=ACTIONS, y=actionsDF["blue_actions"],
    name=Main.BLUE, marker_color=Main.BLUE_COLOR_PRIMARY,
    visible=True
)

fig.add_bar(
    x=ACTIONS, y=actionsDF["blue_free_actions"],
    name=Main.BLUE, marker_color=Main.BLUE_COLOR_PRIMARY,
    visible=False
)

fig.add_bar(
    x=ACTIONS, y=actionsDF["red_all_actions"],
    name=Main.RED, marker_color=Main.RED_COLOR_PRIMARY,
    visible=False
)
fig.add_bar(
    x=ACTIONS, y=actionsDF["red_actions"],
    name=Main.RED, marker_color=Main.RED_COLOR_PRIMARY,
    visible=True
)
fig.add_bar(
    x=ACTIONS, y=actionsDF["red_free_actions"],
    name=Main.RED, marker_color=Main.RED_COLOR_PRIMARY,
    visible=False
)

fig.update_layout(
    bargap=0, bargroupgap=0,
    title = "Actions Performed",
    yaxis_title = "Count",
    xaxis_title = "Type",
    updatemenus=[
        dict(
            type="buttons",
            direction="right",
            active=1,
            x=0.57,
            y=1.2,
            buttons=list([
                dict(label="Free Actions",
                        method="update",
                        args=[{"visible": [False, False, True, False, False, True]},
                            {"title": "Free Actions"}]),
                dict(label="Actions",
                        method="update",
                        args=[{"visible": [False, True, False, False, True, False]},
                            {"title": "Actions"}]),
                dict(label="All",
                        method="update",
                        args=[{"visible": [True, False, False, True, False, False]},
                            {"title": "All Actions"}]),
            ]),
        )
    ]
)

fig.show()

fig.write_html(Main.DATAPATH.joinpath("Charts\\Actions.html"))
