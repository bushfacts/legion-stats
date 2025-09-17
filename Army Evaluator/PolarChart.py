#goes CCW from +x axis

import plotly.graph_objects as go
import pandas as pd
import Functions


firePower1 = Functions.FirePower("Army Evaluator\\Data\\sample.json")
firePower2 = Functions.FirePower("Army Evaluator\\Data\\sample2.json")
firePower3 = Functions.FirePower("Army Evaluator\\Data\\sample3.json")
firePower4 = Functions.FirePower("Army Evaluator\\Data\\sample4.json")

halfCircle = [180 - i*180/5 for i in range(6)]
quarterCircle = [135 - i*90/5 for i in range(6)]

fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r=firePower1,
    theta=halfCircle,
    fill='toself',
    # fillcolor='red'
))
fig.add_trace(go.Scatterpolar(
    r=firePower2,
    theta=halfCircle,
    fill='toself',
    # fillcolor='blue'
))
fig.add_trace(go.Scatterpolar(
    r=firePower3,
    theta=halfCircle,
    fill='toself',
    # fillcolor='green'
))
# fig.add_trace(go.Scatterpolar(
#     r=firePower4,
#     theta=halfCircle,
#     fill='toself',
#     # fillcolor='green'
# ))


fig.update_layout(
  polar=dict(
    radialaxis=dict(
      visible=True
    ),
  ),
  showlegend=False
)

fig.show()
