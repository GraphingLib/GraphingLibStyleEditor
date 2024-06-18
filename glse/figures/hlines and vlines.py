import graphinglib as gl

hlines = gl.Hlines(y=[0.5, 0.75], x_min=0, x_max=1)

vlines = gl.Vlines(x=[0.5, 0.75], y_min=0, y_max=1)

fig = gl.Figure()
fig.add_elements(hlines, vlines)
fig.show()
