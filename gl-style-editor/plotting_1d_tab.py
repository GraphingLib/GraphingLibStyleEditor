from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QTabWidget,
    QWidget,
    QScrollArea,
    QLabel,
    QFrame,
    QMainWindow,
)

from .widgets import ColorPickerWidget, Slider, Activator, Dropdown


def create_plotting_1d_tab(window: QMainWindow):
    layout = QVBoxLayout()
    tabWidget = QTabWidget()

    # curve tab
    curveTabLayout = create_curve_tab(window)
    curveTab = QWidget()
    curveTab.setLayout(curveTabLayout)
    curveTabScrollArea = QScrollArea()
    curveTabScrollArea.setWidgetResizable(True)
    curveTabScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    curveTabScrollArea.setWidget(curveTab)
    tabWidget.addTab(curveTabScrollArea, "Curve")

    # scatter tab
    scatterTabLayout = create_scatter_tab(window)
    scatterTab = QWidget()
    scatterTab.setLayout(scatterTabLayout)
    scatterTabScrollArea = QScrollArea()
    scatterTabScrollArea.setWidgetResizable(True)
    scatterTabScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    scatterTabScrollArea.setWidget(scatterTab)
    tabWidget.addTab(scatterTabScrollArea, "Scatter")

    # histogram tab
    histogramTab = QWidget()
    tabWidget.addTab(histogramTab, "Histogram")

    layout.addWidget(tabWidget)
    window.plotting1DTab.setLayout(layout)


def create_curve_tab(window: QMainWindow):
    # Create a layout for the curve sub-tab
    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignTop)

    # section for curve
    curve_label = QLabel("Curve:")
    curve_label.setStyleSheet("font-weight: bold;")
    layout.addWidget(curve_label)

    curve_line = QFrame()
    curve_line.setFrameShape(QFrame.HLine)
    curve_line.setFrameShadow(QFrame.Sunken)
    layout.addWidget(curve_line)

    # create line_width slider
    line_width_slider = Slider(
        window,
        "Line Width:",
        0,
        20,
        1,
        ["Curve", "line_width"],
    )
    layout.addWidget(line_width_slider)

    # create linestyle drop down menu
    line_style_dropdown = Dropdown(
        window,
        "Line Style:",
        ["Solid", "Dashed", "Dotted", "Dash-Dot"],
        ["-", "--", ":", "-."],
        ["Curve", "line_style"],
    )
    layout.addWidget(line_style_dropdown)

    # create fill under color picker and "same as curve" checkbox
    initial_fill_under_color = (
        "#000000"
        if window.params["Curve"]["fill_under_color"] == "same as curve"
        else window.params["Curve"]["fill_under_color"]
    )
    fill_under_color = ColorPickerWidget(
        window,
        "Fill Under",
        initial_fill_under_color,
        param_ids=["Curve", ["fill_under_color"]],
        activated_on_init=False,
    )
    fill_under_color_checkbox = Activator(
        window,
        fill_under_color,
        ["Curve", "fill_under_color"],
    )
    layout.addWidget(fill_under_color_checkbox)

    # create line cap style dropdown
    line_cap_style_dropdown = Dropdown(
        window,
        "Line Cap Style:",
        ["Squared", "Rounded", "Squared extended"],
        ["butt", "round", "projecting"],
        ["rc_params", "lines.solid_capstyle"],
    )
    layout.addWidget(line_cap_style_dropdown)

    # create dash cap style dropdown
    dash_cap_style_dropdown = Dropdown(
        window,
        "Dash Cap Style:",
        ["Squared", "Rounded", "Squared extended"],
        ["butt", "round", "projecting"],
        ["rc_params", "lines.dash_capstyle"],
    )
    layout.addWidget(dash_cap_style_dropdown)

    # create dashed join style dropdown
    dash_join_style_dropdown = Dropdown(
        window,
        "Dash Join Style:",
        ["Squared", "Rounded", "Beveled"],
        ["miter", "round", "bevel"],
        ["rc_params", "lines.dash_joinstyle"],
    )
    layout.addWidget(dash_join_style_dropdown)

    # section for curve errorbars
    errorbar_label = QLabel("Errorbars:")
    errorbar_label.setStyleSheet("font-weight: bold;")
    layout.addWidget(errorbar_label)

    errorbar_line = QFrame()
    errorbar_line.setFrameShape(QFrame.HLine)
    errorbar_line.setFrameShadow(QFrame.Sunken)
    layout.addWidget(errorbar_line)

    # create errorbar cap width slider
    cap_width_slider = Slider(window, "Cap Width:", 0, 20, 1, ["Curve", "cap_width"])
    layout.addWidget(cap_width_slider)

    # create errorbar color button and "same as curve" checkbox
    errorbars_initial_color = (
        "#000000"
        if window.params["Curve"]["errorbars_color"] == "same as curve"
        else window.params["Curve"]["errorbars_color"]
    )
    errorbars_color = ColorPickerWidget(
        window,
        "Color",
        errorbars_initial_color,
        ["Curve", ["errorbars_color"]],
        activated_on_init=window.params["Curve"]["errorbars_color"] != "same as curve",
    )
    errorbars_color_checkbox = Activator(
        window,
        errorbars_color,
        param_ids=["Curve", "errorbars_color"],
    )
    layout.addWidget(errorbars_color_checkbox)

    # create errorbars line width slider and "same as curve" checkbox
    errorbars_line_width_slider = Slider(
        window,
        "Line Width:",
        0,
        20,
        1,
        ["Curve", "errorbars_line_width"],
    )
    errorbars_line_width_checkbox = Activator(
        window,
        errorbars_line_width_slider,
        param_ids=["Curve", "errorbars_line_width"],
    )
    layout.addWidget(errorbars_line_width_checkbox)

    # create errorbars cap thickness slider and "same as curve" checkbox
    cap_thickness_slider = Slider(
        window,
        "Cap Thickness:",
        0,
        20,
        1,
        ["Curve", "cap_thickness"],
    )
    cap_thickness_checkbox = Activator(
        window,
        cap_thickness_slider,
        ["Curve", "cap_thickness"],
    )
    layout.addWidget(cap_thickness_checkbox)

    return layout


def create_scatter_tab(window: QMainWindow):
    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignTop)

    scatter_label = QLabel("Scatter:")
    scatter_label.setStyleSheet("font-weight: bold;")
    layout.addWidget(scatter_label)

    scatter_line = QFrame()
    scatter_line.setFrameShape(QFrame.HLine)
    scatter_line.setFrameShadow(QFrame.Sunken)
    layout.addWidget(scatter_line)

    marker_edge_color = ColorPickerWidget(
        window,
        "Marker Edge Color:",
        window.params["Scatter"]["edge_color"],
        ["Scatter", ["edge_color"]],
        activated_on_init=(
            False if window.params["Scatter"]["edge_color"] == "none" else True
        ),
    )
    marker_edge_color_checkbox = Activator(
        window, marker_edge_color, ["Scatter", "edge_color"], True
    )
    layout.addWidget(marker_edge_color_checkbox)

    marker_size_slider = Slider(
        window, "Marker Size:", 0, 200, 10, ["Scatter", "marker_size"]
    )
    layout.addWidget(marker_size_slider)

    marker_style_dropdown = Dropdown(
        window,
        "Marker Style:",
        [
            "Circle",
            "Triangle Up",
            "Triangle Down",
            "Triangle Left",
            "Triangle Right",
            "Square",
            "X",
            "Thin Diamond",
        ],
        ["o", "^", "v", "<", ">", "s", "x", "d"],
        ["Scatter", "marker_style"],
    )
    layout.addWidget(marker_style_dropdown)

    errorbar_label = QLabel("Errorbars:")
    errorbar_label.setStyleSheet("font-weight: bold;")
    layout.addWidget(errorbar_label)

    errorbar_line = QFrame()
    errorbar_line.setFrameShape(QFrame.HLine)
    errorbar_line.setFrameShadow(QFrame.Sunken)
    layout.addWidget(errorbar_line)

    errorbars_intitial_color = (
        "#000000"
        if "same as" in window.params["Scatter"]["errorbars_color"]
        else window.params["Scatter"]["errorbars_color"]
    )
    errorbars_color = ColorPickerWidget(
        window,
        "Color:",
        errorbars_intitial_color,
        ["Scatter", ["errorbars_color"]],
        "same as" not in window.params["Scatter"]["errorbars_color"],
    )
    errorbars_color_checkbox = Activator(
        window, errorbars_color, ["Scatter", "errorbars_color"]
    )
    layout.addWidget(errorbars_color_checkbox)

    cap_width_slider = Slider(window, "Cap Width:", 0, 20, 1, ["Scatter", "cap_width"])
    layout.addWidget(cap_width_slider)

    errorbars_line_width = Slider(
        window, "Line Width:", 0, 20, 1, ["Scatter", "errorbars_line_width"]
    )
    layout.addWidget(errorbars_line_width)

    errorbars_cap_thickness = Slider(
        window, "Cap Thickness:", 0, 20, 1, ["Scatter", "cap_thickness"]
    )
    layout.addWidget(errorbars_cap_thickness)

    return layout
