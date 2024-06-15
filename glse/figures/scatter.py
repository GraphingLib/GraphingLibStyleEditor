import graphinglib as gl

curve1 = gl.Scatter.from_function(
    lambda x: x**3 - 2 * x**2 + x,
    x_min=-1,
    x_max=2,
    label="Data 1",
    number_of_points=10,
)

curve2 = gl.Scatter.from_function(
    lambda x: x**3 - 2 * x**2 + x + 3,
    x_min=-1,
    x_max=2,
    label="Data 2",
    number_of_points=10,
)

curve2.add_errorbars(x_error=0.1, y_error=1)

fig = gl.Figure()
fig.add_elements(curve1, curve2)
fig.show()
