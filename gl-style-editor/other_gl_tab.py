from turtle import color

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QScrollArea, QTabWidget, QVBoxLayout, QWidget

from .widgets import Activator, ColorPickerWidget, Dropdown, Slider


def create_other_gl_tab(window):
    layout = QVBoxLayout()
    tabWidget = QTabWidget()

    pointTabLayout = create_point_tab(window)
    pointTab = QWidget()
    pointTab.setLayout(pointTabLayout)
    pointTabScrollArea = QScrollArea()
    pointTabScrollArea.setWidgetResizable(True)
    pointTabScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    pointTabScrollArea.setWidget(pointTab)
    tabWidget.addTab(pointTabScrollArea, "Point")

    # Example stubs for each sub-tab
    hlinesVlinesTab = QWidget()
    tabWidget.addTab(hlinesVlinesTab, "Hlines and Vlines")
    pointTab = QWidget()
    tabWidget.addTab(pointTab, "Point")
    textTab = QWidget()
    tabWidget.addTab(textTab, "Text")
    tableTab = QWidget()
    tabWidget.addTab(tableTab, "Table")

    layout.addWidget(tabWidget)
    window.otherGLTab.setLayout(layout)


def create_point_tab(window):
    # create layout
    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignTop)

    initial_color = (
        "#000000"
        if window.params["Point"]["color"] == "none"
        else window.params["Point"]["color"]
    )
    colorPicker = ColorPickerWidget(
        window=window,
        label="Fill color",
        initial_color=initial_color,
        param_ids=["Point", ["color"]],
        activated_on_init=(initial_color == "none"),
    )
    color_activator = Activator(
        window=window,
        widget=colorPicker,
        param_ids=["Point", "color"],
        check_label="No fill",
        param_if_checked="none",
    )
    layout.addWidget(color_activator)

    edge_initial_color = (
        "#000000"
        if window.params["Point"]["edge_color"] == "none"
        else window.params["Point"]["edge_color"]
    )
    edge_colorpicker = ColorPickerWidget(
        window=window,
        label="Edge Color",
        initial_color=edge_initial_color,
        param_ids=["Point", ["edge_color"]],
        activated_on_init=True,
    )
    edge_color_activator = Activator(
        window=window,
        widget=edge_colorpicker,
        param_ids=["Point", "edge_color"],
        check_label="No edge",
        param_if_checked="none",
    )
    layout.addWidget(edge_color_activator)

    # edge_width
    edge_width_slider = Slider(
        window=window,
        label="Edge Width",
        mini=0,
        maxi=10,
        tick_interval=1,
        param_ids=["Point", "edge_width"],
        conversion_factor=1,
    )
    layout.addWidget(edge_width_slider)

    # marker_size
    marker_size_slider = Slider(
        window=window,
        label="Marker Size",
        mini=0,
        maxi=100,
        tick_interval=5,
        param_ids=["Point", "marker_size"],
        conversion_factor=1,
    )
    layout.addWidget(marker_size_slider)

    # marker_style
    marker_style_dropdown = Dropdown(
        window=window,
        label="Marker Style",
        items=["circle", "x", "+", "square", "diamond"],
        param_values=["o", "x", "+", "s", "d"],
        param_ids=["Point", "marker_style"],
    )
    layout.addWidget(marker_style_dropdown)

    return layout
