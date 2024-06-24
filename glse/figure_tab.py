from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QLabel, QMainWindow, QVBoxLayout

from .widgets import (
    Activator,
    CheckBox,
    ColorPickerWidget,
    Dropdown,
    Slider,
    TableWidget,
)


def create_figure_tab(window: QMainWindow):
    figureTabLayout = QVBoxLayout()
    figureTabLayout.setAlignment(Qt.AlignTop)

    # Section for general figure settings
    figure_label = QLabel("General Figure Settings:")
    figure_label.setStyleSheet("font-weight: bold;")
    figureTabLayout.addWidget(figure_label)

    figure_line = QFrame()
    figure_line.setFrameShape(QFrame.HLine)
    figure_line.setFrameShadow(QFrame.Sunken)
    figureTabLayout.addWidget(figure_line)

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

    # axes label color
    axes_label_color_widget = ColorPickerWidget(
        window,
        label="Axis Labels Color:",
        param_ids=["rc_params", ["axes.labelcolor"]],
        initial_color=window.params["rc_params"]["axes.labelcolor"],
    )
    figureTabLayout.addWidget(axes_label_color_widget)

    # axes line width
    axes_line_width_slider = Slider(
        window, "Axes Line Width:", 0, 20, 1, ["rc_params", "axes.linewidth"]
    )
    figureTabLayout.addWidget(axes_line_width_slider)

    # Section for axes ticks
    ticks_label = QLabel("Ticks:")
    ticks_label.setStyleSheet("font-weight: bold;")
    figureTabLayout.addWidget(ticks_label)

    ticks_line = QFrame()
    ticks_line.setFrameShape(QFrame.HLine)
    ticks_line.setFrameShadow(QFrame.Sunken)
    figureTabLayout.addWidget(ticks_line)

    # ticks color
    axes_ticks_color_widget = ColorPickerWidget(
        window,
        label="Ticks Color:",
        param_ids=["rc_params", ["xtick.color", "ytick.color"]],
        initial_color=window.params["rc_params"]["xtick.color"],
    )
    figureTabLayout.addWidget(axes_ticks_color_widget)

    # ticks direction
    ticks_direction_dropdown = Dropdown(
        window,
        "Ticks Direction:",
        ["In", "Out", "In/Out"],
        ["in", "out", "inout"],
        ["rc_params", ["xtick.direction", "ytick.direction"]],
    )
    figureTabLayout.addWidget(ticks_direction_dropdown)

    # Section for legend
    legend_label = QLabel("Legend:")
    legend_label.setStyleSheet("font-weight: bold;")
    figureTabLayout.addWidget(legend_label)

    legend_line = QFrame()
    legend_line.setFrameShape(QFrame.HLine)
    legend_line.setFrameShadow(QFrame.Sunken)
    figureTabLayout.addWidget(legend_line)

    # legend face color
    legend_face_color_widget = ColorPickerWidget(
        window,
        label="Legend Face Color:",
        param_ids=["rc_params", ["legend.facecolor"]],
        initial_color=window.params["rc_params"]["legend.facecolor"],
    )
    figureTabLayout.addWidget(legend_face_color_widget)

    # legend edge color
    legend_edge_color_widget = ColorPickerWidget(
        window,
        label="Legend Edge Color:",
        param_ids=["rc_params", ["legend.edgecolor"]],
        initial_color=(
            window.params["rc_params"]["legend.edgecolor"]
            if window.params["rc_params"]["legend.edgecolor"] != "none"
            else "#000000"
        ),
    )

    legend_edge_color_activator = Activator(
        window,
        legend_edge_color_widget,
        param_ids=["rc_params", ["legend.edgecolor"]],
        check_label="None",
        param_if_checked="none",
    )

    figureTabLayout.addWidget(legend_edge_color_activator)

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

    # grid alpha
    axes_grid_alpha_slider = Slider(
        window,
        "Grid Opacity:",
        0,
        10,
        1,
        ["rc_params", "grid.alpha"],
        conversion_factor=10,
    )
    figureTabLayout.addWidget(axes_grid_alpha_slider)

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

    # Text Section
    text_label = QLabel("Text:")
    text_label.setStyleSheet("font-weight: bold;")
    figureTabLayout.addWidget(text_label)

    text_line = QFrame()
    text_line.setFrameShape(QFrame.HLine)
    text_line.setFrameShadow(QFrame.Sunken)
    figureTabLayout.addWidget(text_line)

    # font family
    font_family_dropdown = Dropdown(
        window,
        "Font Family:",
        ["Sans-serif", "Serif", "Monospace"],
        ["sans-serif", "serif", "monospace"],
        ["rc_params", "font.family"],
    )
    figureTabLayout.addWidget(font_family_dropdown)

    # font size
    font_size_slider = Slider(
        window, "Font Size:", 0, 30, 1, ["rc_params", "font.size"]
    )
    figureTabLayout.addWidget(font_size_slider)

    # font weight (doesn't work with title and axis labels)
    # font_weight_dropdown = Dropdown(
    #     window,
    #     "Font Weight:",
    #     ["Normal", "Bold"],
    #     ["normal", "bold"],
    #     ["rc_params", "font.weight"],
    # )
    # figureTabLayout.addWidget(font_weight_dropdown)

    # Additional settings
    additional_label = QLabel("Additional Settings:")
    additional_label.setStyleSheet("font-weight: bold;")
    figureTabLayout.addWidget(additional_label)

    additional_line = QFrame()
    additional_line.setFrameShape(QFrame.HLine)
    additional_line.setFrameShadow(QFrame.Sunken)
    figureTabLayout.addWidget(additional_line)

    # Explanation for additional settings
    additional_label = QLabel("Enter any additional rcParams here:")
    figureTabLayout.addWidget(additional_label)

    table = TableWidget(
        window,
        initial_dict=window.params["rc_params"],
    )
    figureTabLayout.addWidget(table)

    return figureTabLayout


def axes_grid_on_clicked(window, state):
    rc = {"axes.grid": True if state == 2 else False}
    window.params["rc_params"].update(rc)
    window.updateFigure()
