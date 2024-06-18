import graphinglib as gl

point1 = gl.Point(x=1, y=1, label="Point A")

point2 = gl.Point(x=3, y=2, label="Point B", h_align="right")

point3 = gl.Point(x=1.25, y=2.25)

point2.add_coordinates()
point3.add_coordinates()

fig = gl.Figure(y_lim=(0.75, 2.5))
fig.add_elements(point1, point2, point3)
fig.show()
