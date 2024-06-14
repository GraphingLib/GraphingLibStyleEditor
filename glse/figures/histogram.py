import graphinglib as gl
import numpy as np

# Create a histogram

np.random.seed(0)
data = np.random.normal(0, 1, 1000)

hist = gl.Histogram(data=data, number_of_bins=20)
hist.add_pdf()

fig = gl.Figure()
fig.add_elements(hist)
fig.show()
