import graphinglib as gl

# Create a stream plot

stream = gl.Stream.from_function(
    lambda x, y: (y, -x), x_axis_range=(-3, 3), y_axis_range=(-3, 3)
)

fig = gl.Figure()
fig.add_elements(stream)
fig.show()
