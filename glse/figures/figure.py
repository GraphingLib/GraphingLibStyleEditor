import graphinglib as gl

# Create a curve

curve = gl.Curve.from_function(
    lambda x: x**3 - 2 * x**2 + x, x_min=-1, x_max=2, label="Data"
)

fig = gl.Figure(title="Figure with curve", x_label="Position [m]", y_label="Force [N]")
fig.add_elements(curve)

fig.show()
