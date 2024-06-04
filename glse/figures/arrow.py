import graphinglib as gl

# Create an arrow
arrow = gl.Arrow(
    pointA=(0, 0),
    pointB=(1, 1),
)

arrow_2 = gl.Arrow(
    pointA=(0, 0),
    pointB=(1, 0),
)

arrow_3 = gl.Arrow(
    pointA=(0, 0),
    pointB=(0, 1),
)

fig = gl.Figure(y_lim=(-0.5, 1.5), x_lim=(-0.5, 1.5))
fig.add_elements(arrow, arrow_2, arrow_3)
fig.show()
