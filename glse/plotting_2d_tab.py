from matplotlib import colormaps
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QMainWindow,
    QScrollArea,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from .widgets import (
    Activator,
    CheckBox,
    ColorPickerWidget,
    Dropdown,
    ListOptions,
    Slider,
)


def create_plotting_2d_tab(window: QMainWindow):
    layout = QVBoxLayout()
    tabWidget = QTabWidget()

    # contour tab
    contourTabLayout = create_contour_tab(window)
    contourTab = QWidget()
    contourTab.setLayout(contourTabLayout)
    contourTabScrollArea = QScrollArea()
    contourTabScrollArea.setWidgetResizable(True)
    contourTabScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    contourTabScrollArea.setWidget(contourTab)
    tabWidget.addTab(contourTabScrollArea, "Contour")

    # heatmap tab
    heatmapTabLayout = create_heatmap_tab(window)
    heatmapTab = QWidget()
    heatmapTab.setLayout(heatmapTabLayout)
    heatmapTabScrollArea = QScrollArea()
    heatmapTabScrollArea.setWidgetResizable(True)
    heatmapTabScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    heatmapTabScrollArea.setWidget(heatmapTab)
    tabWidget.addTab(heatmapTabScrollArea, "Heatmap")

    # stream tab
    streamTabLayout = create_stream_tab(window)
    streamTab = QWidget()
    streamTab.setLayout(streamTabLayout)
    streamTabScrollArea = QScrollArea()
    streamTabScrollArea.setWidgetResizable(True)
    streamTabScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    streamTabScrollArea.setWidget(streamTab)
    tabWidget.addTab(streamTabScrollArea, "Stream")

    # Example stubs for each sub-tab
    vectorFieldTab = QWidget()
    tabWidget.addTab(vectorFieldTab, "VectorField")

    layout.addWidget(tabWidget)
    window.plotting2DTab.setLayout(layout)

    return tabWidget


def create_contour_tab(window: QMainWindow):
    # Create a layout for the contour tab
    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignTop)

    # create colormap dropdown
    colormap = ListOptions(
        window,
        "Colormap",
        list(colormaps),
        ["Contour", "_color_map"],
    )
    layout.addWidget(colormap)

    # create number_of_levels slider
    levels = Slider(
        window,
        "Number of Levels",
        1,
        50,
        2,
        ["Contour", "_number_of_levels"],
        conversion_factor=1,
    )
    layout.addWidget(levels)

    # create alpha slider
    alpha = Slider(
        window,
        "Opacity",
        0,
        100,
        5,
        ["Contour", "_alpha"],
        conversion_factor=100,
    )
    layout.addWidget(alpha)

    # create show_color_bar checkbox
    show_colorbar = CheckBox(
        window,
        "Show Colorbar",
        ["Contour", "_show_color_bar"],
    )
    layout.addWidget(show_colorbar)

    # create filled checkbox
    filled = CheckBox(
        window,
        "Filled",
        ["Contour", "_filled"],
    )
    layout.addWidget(filled)

    return layout


def create_heatmap_tab(window: QMainWindow):
    # Create a layout for the heatmap tab
    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignTop)

    # create colormap dropdown
    colormap = ListOptions(
        window,
        "Colormap",
        list(colormaps),
        ["Heatmap", "_color_map"],
    )
    layout.addWidget(colormap)

    # create origin position dropdown
    origin = Dropdown(
        window,
        label="Origin position",
        items=["Upper left", "Lower left"],
        param_values=["upper", "lower"],
        param_ids=["Heatmap", "_origin_position"],
    )
    layout.addWidget(origin)

    # create aspect ratio dropdown
    aspect_ratio = Dropdown(
        window,
        "Aspect ratio",
        ["Fit data to axes", "Fit axes to data (equal)"],
        ["auto", "equal"],
        ["Heatmap", "_aspect_ratio"],
    )
    layout.addWidget(aspect_ratio)

    return layout


def create_stream_tab(window: QMainWindow):

    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignTop)

    # create line_width slider
    line_width = Slider(
        window,
        "Line Width",
        0,
        10,
        1,
        ["Stream", "_line_width"],
        conversion_factor=1,
    )
    layout.addWidget(line_width)

    # create arrow_size slider
    arrow_size = Slider(
        window,
        "Arrow Size",
        0,
        10,
        1,
        ["Stream", "_arrow_size"],
        conversion_factor=1,
    )
    layout.addWidget(arrow_size)

    # create colormap dropdown
    colormap = ListOptions(
        window,
        "Colormap",
        list(colormaps),
        ["Stream", "_color_map"],
    )
    layout.addWidget(colormap)

    # create color button with activator
    initial_color = (
        "#000000"
        if window.params["Stream"]["_color"] is None
        else window.params["Stream"]["_color"]
    )
    color = ColorPickerWidget(
        window,
        "Color",
        initial_color=initial_color,
        param_ids=["Stream", ["_color"]],
        activated_on_init=window.params["Stream"]["_color"] is not None,
    )
    activator = Activator(
        window,
        color,
        param_ids=["Stream", "_color"],
        check_label="Use color cycle",
        param_if_checked=None,
    )
    layout.addWidget(activator)

    return layout
