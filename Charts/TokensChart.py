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

TOKENS = ["Aim", "Dodge", "Surge", "Standby"]

#region Get and Sort Free Actions
redTokenCounts = [0 for i in range(len(TOKENS))]
blueTokenCounts = [0 for i in range(len(TOKENS))]
for index, row in df.iterrows():
    freeTokens = row["Free Tokens"]
    if not pd.isnull(freeTokens):
        freeTokens = freeTokens.split("//")
        for token in freeTokens:
            index = TOKENS.index(token)
            if row["Player"] == "Blue":
                blueTokenCounts[index] = blueTokenCounts[index] + 1
            else:
                redTokenCounts[index] = redTokenCounts[index] + 1
#endregion

actionsDF = pd.DataFrame({
    "red_tokens": redTokenCounts,
    "blue_tokens": blueTokenCounts
})

fig = go.Figure()

fig.add_bar(
    x=TOKENS, y=actionsDF["blue_tokens"],
    name=Main.BLUE, marker_color=Main.BLUE_COLOR_PRIMARY
)

fig.add_bar(
    x=TOKENS, y=actionsDF["red_tokens"],
    name=Main.RED, marker_color=Main.RED_COLOR_PRIMARY
)

fig.update_layout(
    bargap=0, bargroupgap=0,
    title = "Free Tokens Gained",
    yaxis_title = "Count",
    xaxis_title = "Token"
)

fig.show()
fig.write_html(Main.DATAPATH.joinpath("Charts\\Free Tokens.html"))
