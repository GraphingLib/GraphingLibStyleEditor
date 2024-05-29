import graphinglib as gl

curve = gl.Curve([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
curve2 = gl.Curve([0, 1, 2, 3, 4], [11, 2, 21, 4, 41]) + 1
curve3 = gl.Curve([0, 1, 2, 3, 4], [12, 3, 22, 5, 42]) + 2

fig = gl.Figure()
fig.add_elements(curve, curve2, curve3)
fig.show()
