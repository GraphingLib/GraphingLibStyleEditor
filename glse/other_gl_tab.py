from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QScrollArea,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from .widgets import Activator, ColorPickerWidget, Dropdown, Slider


def create_other_gl_tab(window):
    layout = QVBoxLayout()
    tabWidget = QTabWidget()

    # point tab
    pointTabLayout = create_point_tab(window)
    pointTab = QWidget()
    pointTab.setLayout(pointTabLayout)
    pointTabScrollArea = QScrollArea()
    pointTabScrollArea.setWidgetResizable(True)
    pointTabScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    pointTabScrollArea.setWidget(pointTab)
    tabWidget.addTab(pointTabScrollArea, "Point")

    # text tab
    textTabLayout = create_text_tab(window)
    textTab = QWidget()
    textTab.setLayout(textTabLayout)
    textTabScrollArea = QScrollArea()
    textTabScrollArea.setWidgetResizable(True)
    textTabScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    textTabScrollArea.setWidget(textTab)
    tabWidget.addTab(textTabScrollArea, "Text")

    # table tab
    tableTabLayout = create_table_tab(window)
    tableTab = QWidget()
    tableTab.setLayout(tableTabLayout)
    tableTabScrollArea = QScrollArea()
    tableTabScrollArea.setWidgetResizable(True)
    tableTabScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    tableTabScrollArea.setWidget(tableTab)
    tabWidget.addTab(tableTabScrollArea, "Table")

    # Hlines and Vlines tab
    hlinesVlinesTabLayout = create_hlines_vlines_tab(window)
    hlinesVlinesTab = QWidget()
    hlinesVlinesTab.setLayout(hlinesVlinesTabLayout)
    hlinesVlinesTabScrollArea = QScrollArea()
    hlinesVlinesTabScrollArea.setWidgetResizable(True)
    hlinesVlinesTabScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    hlinesVlinesTabScrollArea.setWidget(hlinesVlinesTab)
    tabWidget.addTab(hlinesVlinesTabScrollArea, "Hlines and Vlines")

    layout.addWidget(tabWidget)
    window.otherGLTab.setLayout(layout)

    return tabWidget


def create_point_tab(window):
    # create layout
    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignTop)

    initial_color = (
        "black"
        if window.params["Point"]["_color"] is None
        else window.params["Point"]["_color"]
    )
    colorPicker = ColorPickerWidget(
        window=window,
        label="Fill color",
        initial_color=initial_color,
        param_ids=["Point", ["_color"]],
        activated_on_init=window.params["Point"]["_color"] is not None,
    )
    color_activator = Activator(
        window=window,
        widget=colorPicker,
        param_ids=["Point", "_color"],
        check_label="No fill",
        param_if_checked=None,
    )
    layout.addWidget(color_activator)

    edge_initial_color = (
        "black"
        if window.params["Point"]["_edge_color"] is None
        else window.params["Point"]["_edge_color"]
    )
    edge_colorpicker = ColorPickerWidget(
        window=window,
        label="Edge Color",
        initial_color=edge_initial_color,
        param_ids=["Point", ["_edge_color"]],
        activated_on_init=window.params["Point"]["_edge_color"] is not None,
    )
    edge_color_activator = Activator(
        window=window,
        widget=edge_colorpicker,
        param_ids=["Point", "_edge_color"],
        check_label="No edge",
        param_if_checked=None,
    )
    layout.addWidget(edge_color_activator)

    # text color picker
    initial_color = (
        window.params["Point"]["_text_color"]
        if window.params["Point"]["_text_color"] != "same as point"
        else "black"
    )
    text_color = ColorPickerWidget(
        window,
        label="Text Color",
        initial_color=initial_color,
        param_ids=["Point", ["_text_color"]],
        activated_on_init=True,
    )
    text_color_activator = Activator(
        window,
        text_color,
        param_ids=["Point", "_text_color"],
        check_label="Same as point",
        param_if_checked="same as point",
    )
    layout.addWidget(text_color_activator)

    # Connect the dropdowns to the color checker functions and pass the window object
    window.point_face_color_checkbox = color_activator
    window.point_edge_color_checkbox = edge_color_activator
    color_activator.checkbox.stateChanged.connect(
        lambda: point_color_checker_face(0, window)
    )
    edge_color_activator.checkbox.stateChanged.connect(
        lambda: point_color_checker_edge(0, window)
    )
    # edge_width
    edge_width_slider = Slider(
        window=window,
        label="Edge Width",
        mini=0,
        maxi=10,
        tick_interval=1,
        param_ids=["Point", "_edge_width"],
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
        param_ids=["Point", "_marker_size"],
        conversion_factor=1,
    )
    layout.addWidget(marker_size_slider)

    # marker_style
    marker_style_dropdown = Dropdown(
        window=window,
        label="Marker Style",
        items=["circle", "x", "+", "square", "thin diamond", "diamond"],
        param_values=["o", "x", "+", "s", "d", "D"],
        param_ids=["Point", "_marker_style"],
    )
    layout.addWidget(marker_style_dropdown)

    return layout


def create_text_tab(window):
    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignTop)

    # create text color picker
    initial_color = window.params["Text"]["_color"]
    color = ColorPickerWidget(
        window,
        "Text Color",
        initial_color=initial_color,
        param_ids=["Text", ["_color"]],
        activated_on_init=True,
    )
    layout.addWidget(color)

    # create halign dropdown
    h_align = Dropdown(
        window,
        label="Horizontal Alignment",
        items=["left", "center", "right"],
        param_values=["left", "center", "right"],
        param_ids=["Text", "_h_align"],
    )
    layout.addWidget(h_align)

    # create valign dropdown
    v_align = Dropdown(
        window,
        label="Vertical Alignment",
        items=["baseline", "bottom", "center", "center baseline", "top"],
        param_values=["baseline", "bottom", "center", "center_baseline", "top"],
        param_ids=["Text", "_v_align"],
    )
    layout.addWidget(v_align)

    return layout


def create_table_tab(window):
    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignTop)

    # cell color picker
    initial_color = window.params["Table"]["_cell_colors"]
    cell_color = ColorPickerWidget(
        window,
        label="Cell Color",
        initial_color=initial_color,
        param_ids=["Table", ["_cell_colors"]],
        activated_on_init=True,
    )
    layout.addWidget(cell_color)

    # col color picker
    initial_color = window.params["Table"]["_col_colors"]
    col_color = ColorPickerWidget(
        window,
        label="Column headers color",
        initial_color=initial_color,
        param_ids=["Table", ["_col_colors"]],
        activated_on_init=True,
    )
    layout.addWidget(col_color)

    # row color picker
    initial_color = window.params["Table"]["_row_colors"]
    row_color = ColorPickerWidget(
        window,
        label="Row headers color",
        initial_color=initial_color,
        param_ids=["Table", ["_row_colors"]],
        activated_on_init=True,
    )
    layout.addWidget(row_color)

    # edge color picker
    initial_color = window.params["Table"]["_edge_color"]
    edge_color = ColorPickerWidget(
        window,
        label="Edge Color",
        initial_color=initial_color,
        param_ids=["Table", ["_edge_color"]],
        activated_on_init=True,
    )
    layout.addWidget(edge_color)

    # edge width slider
    edge_width_slider = Slider(
        window=window,
        label="Edge Width",
        mini=0,
        maxi=20,
        tick_interval=1,
        param_ids=["Table", "_edge_width"],
        conversion_factor=2,
    )
    layout.addWidget(edge_width_slider)

    # text color picker
    initial_color = window.params["Table"]["_text_color"]
    text_color = ColorPickerWidget(
        window,
        label="Text Color",
        initial_color=initial_color,
        param_ids=["Table", ["_text_color"]],
        activated_on_init=True,
    )
    layout.addWidget(text_color)

    # cell align dropdown
    cell_align = Dropdown(
        window,
        label="Text alignment",
        items=["left", "center", "right"],
        param_values=["left", "center", "right"],
        param_ids=["Table", "_cell_align"],
    )
    layout.addWidget(cell_align)

    # row align dropdown
    row_align = Dropdown(
        window,
        label="Row headers alignment",
        items=["left", "center", "right"],
        param_values=["left", "center", "right"],
        param_ids=["Table", "_row_align"],
    )
    layout.addWidget(row_align)

    # col align dropdown
    col_align = Dropdown(
        window,
        label="Column headers alignment",
        items=["left", "center", "right"],
        param_values=["left", "center", "right"],
        param_ids=["Table", "_col_align"],
    )
    layout.addWidget(col_align)

    return layout


def create_hlines_vlines_tab(window):
    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignTop)

    # section for hlines
    hlines_label = QLabel("Hlines:")
    hlines_label.setStyleSheet("font-weight: bold;")
    layout.addWidget(hlines_label)

    hlines_line = QFrame()
    hlines_line.setFrameShape(QFrame.HLine)
    hlines_line.setFrameShadow(QFrame.Sunken)
    layout.addWidget(hlines_line)

    # Color picker for hlines
    initial_color = window.params["Hlines"]["_colors"]
    color = ColorPickerWidget(
        window,
        "Color",
        initial_color=initial_color,
        param_ids=["Hlines", ["_colors"]],
        activated_on_init=True,
    )
    layout.addWidget(color)

    # line width slider for hlines
    line_width_slider = Slider(
        window=window,
        label="Line Width",
        mini=0,
        maxi=20,
        tick_interval=2,
        param_ids=["Hlines", "_line_widths"],
        conversion_factor=2,
    )
    layout.addWidget(line_width_slider)

    # line style dropdown for hlines
    line_style_dropdown = Dropdown(
        window,
        label="Line Style",
        items=["solid", "dashed", "dotted", "dashdot"],
        param_values=["-", "--", ":", "-."],
        param_ids=["Hlines", "_line_styles"],
    )
    layout.addWidget(line_style_dropdown)

    # section for vlines
    vlines_label = QLabel("Vlines:")
    vlines_label.setStyleSheet("font-weight: bold;")
    layout.addWidget(vlines_label)

    vlines_line = QFrame()
    vlines_line.setFrameShape(QFrame.HLine)
    vlines_line.setFrameShadow(QFrame.Sunken)
    layout.addWidget(vlines_line)

    # Color picker for vlines
    initial_color = window.params["Vlines"]["_colors"]
    color = ColorPickerWidget(
        window,
        "Color",
        initial_color=initial_color,
        param_ids=["Vlines", ["_colors"]],
        activated_on_init=True,
    )
    layout.addWidget(color)

    # line width slider for vlines
    line_width_slider = Slider(
        window=window,
        label="Line Width",
        mini=0,
        maxi=20,
        tick_interval=2,
        param_ids=["Vlines", "_line_widths"],
        conversion_factor=2,
    )
    layout.addWidget(line_width_slider)

    # line style dropdown for vlines
    line_style_dropdown = Dropdown(
        window,
        label="Line Style",
        items=["solid", "dashed", "dotted", "dashdot"],
        param_values=["solid", "--", ":", "-."],
        param_ids=["Vlines", "_line_styles"],
    )
    layout.addWidget(line_style_dropdown)

    return layout


def point_color_checker_edge(index, window):
    # Ensures that if edge color is set to none, face color is not set to none. In the case that face color is set to none, it is changed to color cycle.
    if window.point_edge_color_checkbox.checkbox.isChecked():
        if window.point_face_color_checkbox.checkbox.isChecked():
            window.point_face_color_checkbox.checkbox.setChecked(False)


def point_color_checker_face(index, window):
    # Ensures that if face color is set to none, edge color is not set to none. In the case that edge color is set to none, it is changed to color cycle.
    if window.point_face_color_checkbox.checkbox.isChecked():
        if window.point_edge_color_checkbox.checkbox.isChecked():
            window.point_edge_color_checkbox.checkbox.setChecked(False)
