import graphinglib as gl

# Create contour plot

contour = gl.Contour.from_function(
    lambda x, y: x**2 + y**2, x_axis_range=(-10, 10), y_axis_range=(-10, 10)
)

fig = gl.Figure()
fig.add_elements(contour)
fig.show()
