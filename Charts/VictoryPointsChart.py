import plotly.graph_objects as go
import pandas as pd

import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import Main

df = pd.read_csv(Main.DATAPATH.joinpath("VPs.csv"))

bluePrev = []
redPrev = []
for index, row in df.iterrows():
    bluePrev.append(df["Blue Primary"].iloc[0:index].sum() + df["Blue Secondary"].iloc[0:index].sum())
    redPrev.append(df["Red Primary"].iloc[0:index].sum() + df["Red Secondary"].iloc[0:index].sum())
print(bluePrev)
print(redPrev)

df["blue_previously_scored"] = bluePrev
df["red_previously_scored"] = redPrev

fig = go.Figure()

fig.add_bar(
    x=df["Round"], y=df["blue_previously_scored"],
    name="Previously Scored", marker_color=Main.BASE_COLOR, offsetgroup="Blue Player"
)

fig.add_bar(
    x=df["Round"], y=df["Blue Primary"],
    name=Main.BLUE + " Primary", marker_color=Main.BLUE_COLOR_PRIMARY, offsetgroup="Blue Player"
)

fig.add_bar(
    x=df["Round"], y=df["Blue Secondary"],
    name=Main.BLUE + " Secondary", marker_color=Main.BLUE_COLOR_SECONDARY, offsetgroup="Blue Player"
)

fig.add_bar(
    x=df["Round"], y=df["red_previously_scored"],
    name="Previously Scored", marker_color=Main.BASE_COLOR, offsetgroup="Red Player"
)

fig.add_bar(
    x=df["Round"], y=df["Red Primary"],
    name=Main.BLUE + " Primary", marker_color=Main.RED_COLOR_PRIMARY, offsetgroup="Red Player"
)

fig.add_bar(
    x=df["Round"], y=df["Red Secondary"],
    name=Main.BLUE + " Secondary", marker_color=Main.RED_COLOR_SECONDARY, offsetgroup="Red Player"
)

fig.update_layout(
    barmode = "stack",
    title = "Victory Points Scored",
    yaxis_title = "Victory Points",
    xaxis_title = "Round"
)


fig.show()
fig.write_html(Main.DATAPATH.joinpath("Charts\\VPs.html"))
