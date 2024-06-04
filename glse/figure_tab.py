from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QCheckBox, QFrame, QLabel, QMainWindow, QVBoxLayout

from glse.widgets import CheckBox, ColorPickerWidget, Dropdown, Slider


def create_figure_tab(window: QMainWindow):
    figureTabLayout = QVBoxLayout()
    figureTabLayout.setAlignment(Qt.AlignTop)

    # Section for Colors
    colors_label = QLabel("Colors:")
    colors_label.setStyleSheet("font-weight: bold;")
    figureTabLayout.addWidget(colors_label)

    colors_line = QFrame()
    colors_line.setFrameShape(QFrame.HLine)
    colors_line.setFrameShadow(QFrame.Sunken)
    figureTabLayout.addWidget(colors_line)

    # figure face color
    figure_color_widget = ColorPickerWidget(
        window,
        label="Figure Color:",
        param_ids=["rc_params", ["figure.facecolor"]],
        initial_color=window.params["rc_params"]["figure.facecolor"],
    )
    figureTabLayout.addWidget(figure_color_widget)

    # axes face color
    axes_face_color_widget = ColorPickerWidget(
        window,
        label="Axes Face Color:",
        param_ids=["rc_params", ["axes.facecolor"]],
        initial_color=window.params["rc_params"]["axes.facecolor"],
    )
    figureTabLayout.addWidget(axes_face_color_widget)

    # axes edge color
    axes_edge_color_widget = ColorPickerWidget(
        window,
        label="Axes Edge Color:",
        param_ids=["rc_params", ["axes.edgecolor"]],
        initial_color=window.params["rc_params"]["axes.edgecolor"],
    )
    figureTabLayout.addWidget(axes_edge_color_widget)

    # ticks color
    axes_ticks_color_widget = ColorPickerWidget(
        window,
        label="Ticks Color:",
        param_ids=["rc_params", ["xtick.color", "ytick.color"]],
        initial_color=window.params["rc_params"]["xtick.color"],
    )
    figureTabLayout.addWidget(axes_ticks_color_widget)

    # Section for Grid
    grid_label = QLabel("Grid:")
    grid_label.setStyleSheet("font-weight: bold;")
    figureTabLayout.addWidget(grid_label)

    grid_line = QFrame()
    grid_line.setFrameShape(QFrame.HLine)
    grid_line.setFrameShadow(QFrame.Sunken)
    figureTabLayout.addWidget(grid_line)

    # grid on/off checkbox
    grid_on_checkbox = CheckBox(window, "Toggle Grid", ["rc_params", "axes.grid"])
    figureTabLayout.addWidget(grid_on_checkbox)

    # grid color
    axes_grid_color_widget = ColorPickerWidget(
        window,
        label="Grid Color:",
        param_ids=["rc_params", ["grid.color"]],
        initial_color=window.params["rc_params"]["grid.color"],
    )
    figureTabLayout.addWidget(axes_grid_color_widget)

    # grid line width (use slider)
    grid_line_width_slider = Slider(
        window, "Grid Line Width:", 0, 20, 1, ["rc_params", "grid.linewidth"]
    )
    figureTabLayout.addWidget(grid_line_width_slider)

    # grid line style (use dropdown)
    grid_line_style_dropdown = Dropdown(
        window,
        "Grid Line Style:",
        ["Solid", "Dashed", "Dotted", "Dash-Dot"],
        ["-", "--", ":", "-."],
        ["rc_params", "grid.linestyle"],
    )
    figureTabLayout.addWidget(grid_line_style_dropdown)

    return figureTabLayout


def axes_grid_on_clicked(window, state):
    rc = {"axes.grid": True if state == 2 else False}
    window.params["rc_params"].update(rc)
    window.updateFigure()
