import graphinglib as gl
import numpy as np

# Create a pentagon
polygon = gl.Polygon(
    vertices=[
        (0, 0),
        (1, 0),
        (1, 1),
        (0.5, 1.5),
        (0, 1),
    ],
)

# Create a circle
circle = gl.Circle(
    x_center=0.5,
    y_center=0.5,
    radius=0.5,
)
circle.translate(0.7, -0.3)

# Create a rectangle
rectangle = gl.Rectangle(
    x_bottom_left=0,
    y_bottom_left=0,
    width=1,
    height=1,
)
rectangle.translate(-0.7, -0.3)

fig = gl.Figure(x_lim=(-1, 2), y_lim=(-1, 2))
fig.add_elements(polygon, circle, rectangle)
fig.show()
