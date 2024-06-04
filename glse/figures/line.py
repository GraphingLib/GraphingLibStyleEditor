import graphinglib as gl

line = gl.Line(pointA=(0, 0), pointB=(1, 1))
line2 = gl.Line(pointA=(0, 1), pointB=(1, 0), capped_line=True)
line3 = gl.Line(pointA=(0, 2), pointB=(1, 3))
line4 = gl.Line(pointA=(0, 3), pointB=(1, 2), capped_line=True)

fig = gl.Figure()
fig.add_elements(line, line2, line3, line4)
fig.show()
