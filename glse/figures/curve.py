import graphinglib as gl

curve1 = gl.Curve.from_function(
    lambda x: x**3 - 2 * x**2 + x + 6, x_min=-1, x_max=2, label="Data 1"
)

curve2 = gl.Curve.from_function(
    lambda x: x**3 - 2 * x**2 + x + 3, x_min=-1, x_max=2, label="Data 2"
)
curve3 = gl.Curve.from_function(
    lambda x: x**3 - 2 * x**2 + x + 9,
    x_min=-1,
    x_max=2,
    label="Data 3",
    number_of_points=10,
)

curve1.add_error_curves(x_error=1, y_error=1)
curve2.get_area_between(x1=-1, x2=2, fill_between=True)
curve3.add_errorbars(x_error=0.1, y_error=1)

fig = gl.Figure()
fig.add_elements(curve3, curve2, curve1)
fig.show()
