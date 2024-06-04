import graphinglib as gl

scatter = gl.Scatter([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
scatter2 = gl.Scatter([0, 1, 2, 3, 4], [11, 2, 21, 4, 41]) + 1
scatter3 = gl.Scatter([0, 1, 2, 3, 4], [12, 3, 22, 5, 42]) + 2

fig = gl.Figure()
fig.add_elements(scatter, scatter2, scatter3)
fig.show()
