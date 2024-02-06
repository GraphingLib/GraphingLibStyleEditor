from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QFrame,
    QPushButton,
    QComboBox,
    QSlider,
    QMainWindow,
)

from .widgets import ColorPickerWidget, Slider, Dropdown


def create_figure_tab(window: QMainWindow):
    window.figureTabLayout = QVBoxLayout()
    window.figureTabLayout.setAlignment(Qt.AlignTop)

    # Section for Colors
    window.colors_label = QLabel("Colors:")
    window.colors_label.setStyleSheet("font-weight: bold;")
    window.figureTabLayout.addWidget(window.colors_label)

    window.colors_line = QFrame()
    window.colors_line.setFrameShape(QFrame.HLine)
    window.colors_line.setFrameShadow(QFrame.Sunken)
    window.figureTabLayout.addWidget(window.colors_line)

    # figure face color
    window.figure_color_widget = ColorPickerWidget(
        window,
        label="Figure Color:",
        param_ids=["rc_params", ["figure.facecolor"]],
        initial_color=window.params["rc_params"]["figure.facecolor"],
    )
    window.figureTabLayout.addWidget(window.figure_color_widget)

    # axes face color
    window.axes_face_color_widget = ColorPickerWidget(
        window,
        label="Axes Face Color:",
        param_ids=["rc_params", ["axes.facecolor"]],
        initial_color=window.params["rc_params"]["axes.facecolor"],
    )
    window.figureTabLayout.addWidget(window.axes_face_color_widget)

    # axes edge color
    window.axes_edge_color_widget = ColorPickerWidget(
        window,
        label="Axes Edge Color:",
        param_ids=["rc_params", ["axes.edgecolor"]],
        initial_color=window.params["rc_params"]["axes.edgecolor"],
    )
    window.figureTabLayout.addWidget(window.axes_edge_color_widget)

    # ticks color
    window.axes_ticks_color_widget = ColorPickerWidget(
        window,
        label="Ticks Color:",
        param_ids=["rc_params", ["xtick.color", "ytick.color"]],
        initial_color=window.params["rc_params"]["xtick.color"],
    )
    window.figureTabLayout.addWidget(window.axes_ticks_color_widget)

    # Section for Grid
    window.grid_label = QLabel("Grid:")
    window.grid_label.setStyleSheet("font-weight: bold;")
    window.figureTabLayout.addWidget(window.grid_label)

    window.grid_line = QFrame()
    window.grid_line.setFrameShape(QFrame.HLine)
    window.grid_line.setFrameShadow(QFrame.Sunken)
    window.figureTabLayout.addWidget(window.grid_line)

    # grid color
    window.axes_grid_color_widget = ColorPickerWidget(
        window,
        label="Grid Color:",
        param_ids=["rc_params", ["grid.color"]],
        initial_color=window.params["rc_params"]["grid.color"],
    )
    window.figureTabLayout.addWidget(window.axes_grid_color_widget)

    # grid on/off
    window.axes_grid_on_button = QPushButton("Toggle Grid", window)
    window.axes_grid_on_button.clicked.connect(axes_grid_on_clicked)
    window.figureTabLayout.addWidget(window.axes_grid_on_button)

    # grid line width (use slider)
    window.axes_grid_line_width_label = QLabel("Grid Line Width:")
    window.figureTabLayout.addWidget(window.axes_grid_line_width_label)
    window.axes_grid_line_width_slider = QSlider(Qt.Horizontal)  # type: ignore
    window.axes_grid_line_width_slider.setMinimum(0)
    window.axes_grid_line_width_slider.setMaximum(20)
    default_grid_width = int(window.params["rc_params"]["grid.linewidth"] * 2)
    window.axes_grid_line_width_slider.setValue(default_grid_width)
    window.axes_grid_line_width_slider.setTickPosition(QSlider.TicksBelow)
    window.axes_grid_line_width_slider.setTickInterval(1)
    window.axes_grid_line_width_slider.valueChanged.connect(
        axes_grid_line_width_changed
    )
    window.figureTabLayout.addWidget(window.axes_grid_line_width_slider)

    # grid line style (use dropdown)
    window.axes_grid_line_style_label = QLabel("Grid Line Style:")
    window.figureTabLayout.addWidget(window.axes_grid_line_style_label)
    window.axes_grid_line_style_dropdown = QComboBox()
    window.axes_grid_line_style_dropdown.addItem("Solid")
    window.axes_grid_line_style_dropdown.addItem("Dashed")
    window.axes_grid_line_style_dropdown.addItem("Dotted")
    window.axes_grid_line_style_dropdown.addItem("Dash-Dot")
    default_grid_style = window.params["rc_params"]["grid.linestyle"]
    window.axes_grid_line_style_dropdown.setCurrentIndex(
        ["-", "--", ":", "-."].index(default_grid_style)
    )
    window.axes_grid_line_style_dropdown.currentIndexChanged.connect(
        axes_grid_line_style_changed
    )
    window.figureTabLayout.addWidget(window.axes_grid_line_style_dropdown)

    window.figureTab.setLayout(window.figureTabLayout)


def axes_grid_on_clicked(window):
    rc = {"axes.grid": not window.params["rc_params"].get("axes.grid", False)}
    window.params["rc_params"].update(rc)
    window.updateFigure()


def axes_grid_line_width_changed(window, value):
    rc = {"grid.linewidth": value / 2}
    window.params["rc_params"].update(rc)
    window.updateFigure()


def axes_grid_line_style_changed(window, value):
    rc = {"grid.linestyle": ["-", "--", ":", "-."][value]}
    window.params["rc_params"].update(rc)
    window.updateFigure()
