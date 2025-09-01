import plotly.graph_objects as go
import pandas as pd
import json

import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import Main

attackData = []
with open(Main.DATAPATH.joinpath("attack_rolls.json"), "r") as file:
    attackData = json.load(file)

fig = go.Figure()


fig.show()

