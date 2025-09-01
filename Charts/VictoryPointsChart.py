import plotly.graph_objects as go
import pandas as pd

import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import Main

df = pd.read_csv(Main.DATAPATH.joinpath("VPs.csv"))



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
fig.write_html(Main.DATAPATH.joinpath("Charts\\VPs.html"))
