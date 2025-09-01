# data I want to be able to see:
# in the tooltip, the health and the activation cound and the round number and the activation number (out of total for htat round)
# can I add points destroyed to this as well?

import plotly.graph_objects as go
import pandas as pd
import numpy as np

import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import Main

df = pd.read_csv(Main.DATAPATH.joinpath("Health over time.csv"))

df["base"] = df[["Blue Activations","Red Activations"]].min(axis=1)
df["blue_advantage"] = (df["Blue Activations"]-df["Red Activations"]).clip(lower=0)
df["red_advantage"] = (df["Red Activations"]-df["Blue Activations"]).clip(lower=0)

#scale the health to match the max activations
scaleFactor = max(df.max(axis=0)["Red Activations"], df.max(axis=0)["Blue Activations"]) / max(df.max(axis=0)["Red Health"], df.max(axis=0)["Blue Health"])
df["blue_health_scaled"] = df["Blue Health"] * scaleFactor
df["red_health_scaled"] = df["Red Health"] * scaleFactor


fig = go.Figure()

fig.add_bar(
    y=df["base"],
    marker_color=Main.BASE_COLOR
)

fig.add_bar(
    y=df["blue_advantage"],
    name= Main.BLUE + " activations", marker_color=Main.BLUE_COLOR_PRIMARY
)

fig.add_bar(
    y=df["red_advantage"],
    name= Main.RED + " activations", marker_color=Main.RED_COLOR_PRIMARY
)

fig.add_trace(go.Line(
    y=df["blue_health_scaled"],
    name= Main.BLUE + " total health",
    marker_color=Main.BLUE_COLOR_SECONDARY
))

fig.add_trace(go.Line(
    y=df["red_health_scaled"],
    name= Main.RED + " total health",
    marker_color=Main.RED_COLOR_SECONDARY
))

fig.update_layout(
    barmode = "stack",
    bargap=0, bargroupgap=0,
    title = "Health Over Time",
    yaxis_title = "Activations",
    xaxis_title = "Turns"
)

fig.show()
fig.write_html(Main.DATAPATH.joinpath("Charts\\Health over time.html"))

