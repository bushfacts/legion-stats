#toggle between free actions, normal, and all

import plotly.graph_objects as go
import pandas as pd

import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import Main

df = pd.read_csv(Main.DATAPATH.joinpath("Actions.csv"))

ACTIONS = ["Aim", "Dodge", "Move", "Standby", "Attack", "Recover", "Restore", "Force Push", "Jedi Mind Trick", "Knife Throw", "Vader's Might"]
MOVES = ["Withdraw", "Move", "Climb", "Scout"]

#region Get and Sort Actions
redActionCounts = []
blueActionCounts = []
for action in ACTIONS:
    count = len(df[
        (df["Action 1"] == action) &
        (df["Player"] == "Red")
        ])
    count = count + len(df[
        (df["Action 2"] == action) &
        (df["Player"] == "Red")
        ])
    redActionCounts.append(count)
    count = len(df[
        (df["Action 1"] == action) &
        (df["Player"] == "Blue")
        ])
    count = count + len(df[
        (df["Action 2"] == action) &
        (df["Player"] == "Blue")
        ])
    blueActionCounts.append(count)
#endregion

#region Get and Sort Free Actions
redFreeActionCounts = [0 for i in range(len(ACTIONS))]
blueFreeActionCounts = [0 for i in range(len(ACTIONS))]
for index, row in df.iterrows():
    freeActions = row["Free Actions"]
    if not pd.isnull(freeActions):
        freeActions = freeActions.split("//")
        for action in freeActions:
            if action in MOVES:
                index = ACTIONS.index("Move")
                if row["Player"] == "Blue":
                    blueFreeActionCounts[index] = blueFreeActionCounts[index] + 1
                else:
                    redFreeActionCounts[index] = redFreeActionCounts[index] + 1
            else:
                index = ACTIONS.index(action)
                if row["Player"] == "Blue":
                    blueFreeActionCounts[index] = blueFreeActionCounts[index] + 1
                else:
                    redFreeActionCounts[index] = redFreeActionCounts[index] + 1
#endregion

actionsDF = pd.DataFrame({
    "red_actions": redActionCounts,
    "blue_actions": blueActionCounts,
    "red_free_actions": redFreeActionCounts,
    "blue_free_actions": blueFreeActionCounts,
    "red_all_actions": [redActionCounts[i] + redFreeActionCounts[i] for i in range(len(ACTIONS))],
    "blue_all_actions": [blueActionCounts[i] + blueFreeActionCounts[i] for i in range(len(ACTIONS))]
})

fig = go.Figure()

fig.add_bar(
    x=ACTIONS, y=actionsDF["blue_all_actions"],
    name=Main.BLUE, marker_color=Main.BLUE_COLOR_PRIMARY
)

fig.add_bar(
    x=ACTIONS, y=actionsDF["red_all_actions"],
    name=Main.RED, marker_color=Main.RED_COLOR_PRIMARY
)

fig.update_layout(
    bargap=0, bargroupgap=0,
    title = "Actions Performed",
    yaxis_title = "Count",
    xaxis_title = "Action"
)

fig.show()

fig.write_html(Main.DATAPATH.joinpath("Charts\\Actions.html"))