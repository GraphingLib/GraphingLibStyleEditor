import graphinglib as gl

# Create a vector field plot

vector_field = gl.VectorField.from_function(
    lambda x, y: (y, -x), x_axis_range=(-3, 3), y_axis_range=(-3, 3)
)

fig = gl.Figure()
fig.add_elements(vector_field)
fig.show()
