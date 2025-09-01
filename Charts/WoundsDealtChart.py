import plotly.graph_objects as go
import pandas as pd

import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import Main

df = pd.read_csv(Main.DATAPATH.joinpath("Wounds Dealt.csv"))

fig = go.Figure()


fig.show()

