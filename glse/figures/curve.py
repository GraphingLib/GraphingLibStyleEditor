import graphinglib as gl

curve1 = gl.Curve.from_function(
    lambda x: x**3 - 2 * x**2 + x + 9,
    x_min=-1,
    x_max=2,
    label="Data 1",
    number_of_points=10,
)

curve2 = gl.Curve.from_function(
    lambda x: x**3 - 2 * x**2 + x + 6, x_min=-1, x_max=2, label="Data 2"
)

curve3 = gl.Curve.from_function(
    lambda x: x**3 - 2 * x**2 + x + 3, x_min=-1, x_max=2, label="Data 3"
)

curve1.add_errorbars(x_error=0.1, y_error=1)
curve2.add_error_curves(y_error=1)
curve3.get_area_between(x1=-1, x2=2, fill_between=True)

fig = gl.Figure()
fig.add_elements(curve1, curve2, curve3)
fig.show()
