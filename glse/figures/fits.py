import graphinglib as gl
import numpy as np

# Create a scatter

np.random.seed(0)
x = np.linspace(-3, 3, 100)
y = 3 * x**2 + 2 * x + 1 + np.random.normal(0, 1, 100)

scatter = gl.Scatter(x, y, label="Data")

fit = gl.FitFromPolynomial(scatter, degree=2, label="Fit")
fit.show_residual_curves(sigma_multiplier=2)

fig = gl.Figure()
fig.add_elements(scatter, fit)
fig.show()
