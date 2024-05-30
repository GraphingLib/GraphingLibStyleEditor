import graphinglib as gl

# Create heatmap

heatmap = gl.Heatmap.from_function(
    lambda x, y: x**2 + y**2, x_axis_range=(-10, 10), y_axis_range=(-10, 10)
)

fig = gl.Figure()
fig.add_elements(heatmap)
fig.show()
