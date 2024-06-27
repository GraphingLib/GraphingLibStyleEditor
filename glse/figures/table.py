import graphinglib as gl

data = [
    [5, 223.9369, 0.0323],
    [10, 223.9367, 0.0324],
    [15, 223.9367, 0.0325],
    [20, 223.9387, 0.0326],
    [25, 223.9385, 0.0327],
]
columns = ["Time (s)", "Voltage (V)", "Current (A)"]
rows = ["Series 1", "Series 2", "Series 3", "Series 4", "Series 5"]

table = gl.Table(
    cell_text=data,
    col_labels=columns,
    row_labels=rows,
    location="center",
)

figure = gl.Figure(size=(5, 2), remove_axes=True)
figure.add_elements(table)
figure.show()
