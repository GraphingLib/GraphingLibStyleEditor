from PySide6.QtCore import Qt
from PySide6.QtWidgets import QScrollArea, QTabWidget, QVBoxLayout, QWidget

from .widgets import Activator, CheckBox, ColorPickerWidget, Dropdown, Slider


def create_shapes_tab(window):
    layout = QVBoxLayout()
    tabWidget = QTabWidget()

    # polygon tab
    polygonTabLayout = create_polygon_tab(window)
    polygonTab = QWidget()
    polygonTab.setLayout(polygonTabLayout)
    polygonTabScrollArea = QScrollArea()
    polygonTabScrollArea.setWidgetResizable(True)
    polygonTabScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    polygonTabScrollArea.setWidget(polygonTab)
    tabWidget.addTab(polygonTabScrollArea, "Polygon")

    # create arrow tab
    arrowTabLayout = create_arrow_tab(window)
    arrowTab = QWidget()
    arrowTab.setLayout(arrowTabLayout)
    arrowTabScrollArea = QScrollArea()
    arrowTabScrollArea.setWidgetResizable(True)
    arrowTabScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    arrowTabScrollArea.setWidget(arrowTab)
    tabWidget.addTab(arrowTabScrollArea, "Arrow")

    # create line tab
    lineTabLayout = create_line_tab(window)
    lineTab = QWidget()
    lineTab.setLayout(lineTabLayout)
    lineTabScrollArea = QScrollArea()
    lineTabScrollArea.setWidgetResizable(True)
    lineTabScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    lineTabScrollArea.setWidget(lineTab)
    tabWidget.addTab(lineTabScrollArea, "Line")

    layout.addWidget(tabWidget)
    window.shapesTab.setLayout(layout)

    return tabWidget


def create_polygon_tab(window):
    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignTop)

    # create fill checkbox
    fill = CheckBox(window, "Fill", [["Circle", "Rectangle", "Polygon"], "_fill"])
    layout.addWidget(fill)

    # create fill_alpha slider
    fill_alpha = Slider(
        window,
        "Fill Opacity",
        0,
        100,
        5,
        [["Circle", "Rectangle", "Polygon"], "_fill_alpha"],
        conversion_factor=100,
    )
    layout.addWidget(fill_alpha)

    # create line_width slider
    line_width = Slider(
        window,
        "Line Width",
        0,
        10,
        1,
        [["Circle", "Rectangle", "Polygon"], "_line_width"],
        conversion_factor=1,
    )
    layout.addWidget(line_width)

    # create line_style dropdown
    line_style = Dropdown(
        window,
        "Line Style",
        ["Solid", "Dashed", "Dotted", "Dash-Dot", "None"],
        ["-", "--", ":", "-.", "None"],
        [["Circle", "Rectangle", "Polygon"], "_line_style"],
    )
    layout.addWidget(line_style)

    # create fill color picker
    initial_color = (
        window.params["Polygon"]["_fill_color"]
        if window.params["Polygon"]["_fill_color"] is not None
        else "C1"
    )
    color = ColorPickerWidget(
        window,
        "Fill Color",
        param_ids=[["Polygon", "Circle", "Rectangle"], ["_fill_color"]],
        initial_color=initial_color,
        activated_on_init=(
            False if window.params["Polygon"]["_fill_color"] is None else True
        ),
    )
    color_picker_widget = Activator(
        window,
        widget=color,
        param_ids=[["Polygon", "Circle", "Rectangle"], ["_fill_color"]],
        check_label="Use color cycle",
        param_if_checked=None,
    )
    layout.addWidget(color_picker_widget)

    # create edge color picker
    initial_color = (
        window.params["Polygon"]["_edge_color"]
        if window.params["Polygon"]["_edge_color"] is not None
        else "black"
    )
    edge_color = ColorPickerWidget(
        window,
        "Edge Color",
        param_ids=[["Polygon", "Circle", "Rectangle"], ["_edge_color"]],
        initial_color=initial_color,
        activated_on_init=(
            False if window.params["Polygon"]["_edge_color"] is None else True
        ),
    )
    edge_color_picker_widget = Activator(
        window,
        widget=edge_color,
        param_ids=[["Polygon", "Circle", "Rectangle"], ["_edge_color"]],
        check_label="None",
        param_if_checked=None,
    )
    layout.addWidget(edge_color_picker_widget)

    return layout


def create_arrow_tab(window):
    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignTop)

    # create color picker
    color = ColorPickerWidget(
        window,
        "Color",
        param_ids=["Arrow", ["_color"]],
        initial_color=window.params["Arrow"]["_color"],
        activated_on_init=(False if window.params["Arrow"]["_color"] == "" else True),
    )
    layout.addWidget(color)

    # create head_size slider
    head_size = Slider(
        window,
        "Head Size",
        0,
        50,
        1,
        ["Arrow", "_head_size"],
        conversion_factor=10,
    )
    layout.addWidget(head_size)

    # create width slider
    width = Slider(
        window, "Width", 0, 100, 1, ["Arrow", "_width"], conversion_factor=10
    )
    layout.addWidget(width)

    return layout


def create_line_tab(window):
    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignTop)

    # create line color picker
    color = ColorPickerWidget(
        window,
        "Color",
        param_ids=["Line", ["_color"]],
        initial_color=window.params["Line"]["_color"],
        activated_on_init=(False if window.params["Line"]["_color"] == "" else True),
    )
    layout.addWidget(color)

    # create line width slider
    width = Slider(
        window,
        "Width",
        0,
        100,
        1,
        ["Line", "_width"],
        conversion_factor=10,
    )
    layout.addWidget(width)

    # create line capwidth slider
    capwidth = Slider(
        window,
        "Cap Width",
        0,
        100,
        1,
        ["Line", "_cap_width"],
        conversion_factor=10,
    )
    layout.addWidget(capwidth)

    return layout
