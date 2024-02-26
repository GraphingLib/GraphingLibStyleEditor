from matplotlib import colormaps
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QFrame,
    QLabel,
    QMainWindow,
    QScrollArea,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from .widgets import CheckBox, ListOptions, Slider


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

    # Example stubs for each sub-tab
    heatmapTab = QWidget()
    tabWidget.addTab(heatmapTab, "Heatmap")
    streamTab = QWidget()
    tabWidget.addTab(streamTab, "Stream")
    vectorFieldTab = QWidget()
    tabWidget.addTab(vectorFieldTab, "VectorField")

    layout.addWidget(tabWidget)
    window.plotting2DTab.setLayout(layout)


def create_contour_tab(window: QMainWindow):
    # Create a layout for the contour tab
    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignTop)

    # create colormap dropdown
    colormap = ListOptions(
        window,
        "Colormap",
        list(colormaps),
        ["Contour", "color_map"],
    )
    layout.addWidget(colormap)

    # create number_of_levels slider
    levels = Slider(
        window,
        "Number of Levels",
        1,
        50,
        2,
        ["Contour", "number_of_levels"],
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
        ["Contour", "alpha"],
        conversion_factor=100,
    )
    layout.addWidget(alpha)

    # create show_color_bar checkbox
    show_colorbar = CheckBox(
        window,
        "Show Colorbar",
        ["Contour", "show_color_bar"],
    )
    layout.addWidget(show_colorbar)

    # create filled checkbox
    filled = CheckBox(
        window,
        "Filled",
        ["Contour", "filled"],
    )
    layout.addWidget(filled)

    return layout
