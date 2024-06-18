import graphinglib as gl

text1 = gl.Text(x=0.5, y=0.65, text="This is a text element", font_size=12)

text2 = gl.Text(
    x=0.5,
    y=0.35,
    text="Red dots show coordinates\nat which text is placed",
    font_size=12,
)

point1 = gl.Point(x=0.5, y=0.35, marker_size=10, color="red")
point2 = gl.Point(x=0.5, y=0.65, marker_size=10, color="red")

fig = gl.Figure(y_lim=[0, 1])
fig.add_elements(point1, point2, text1, text2)
fig.show()
