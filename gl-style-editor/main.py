import sys

import graphinglib as gl
from matplotlib.pyplot import close
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QApplication,
    QColorDialog,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSlider,
    QSplitter,
    QTabWidget,
    QVBoxLayout,
    QWidget,
    QCheckBox,
)


class ColorButton(QPushButton):
    colorChanged = pyqtSignal(str)

    def __init__(self, *args, color=None, **kwargs):
        super(ColorButton, self).__init__(*args, **kwargs)
        self._color = None
        self._default = color
        self.pressed.connect(self.onColorPicker)
        self.setColor(self._default)
        self.setFixedSize(25, 25)

    def setColor(self, color):
        if color != self._color:
            self._color = color
            self.colorChanged.emit(color)
        if self._color:
            self.setStyleSheet("background-color: %s;" % self._color)
        else:
            self.setStyleSheet("")

    def color(self):
        return self._color

    def onColorPicker(self):
        dlg = QColorDialog(self)
        if self._color:
            dlg.setCurrentColor(QColor(self._color))

        # Calculate the position to move the dialog next to the button
        button_pos = self.mapToGlobal(self.pos())
        dlg.move(button_pos.x(), button_pos.y())

        if dlg.exec_():
            self.setColor(dlg.currentColor().name())

    def mousePressEvent(self, e):
        if e.button() == Qt.RightButton:  # type: ignore
            self.setColor(self._default)
        return super(ColorButton, self).mousePressEvent(e)


class ColorPickerWidget(QWidget):
    def __init__(
        self,
        window: QMainWindow,
        label="Pick a colour:",
        initial_color="#ff0000",
        param_ids=[],
        activated_on_init=True,
    ):
        super().__init__()
        self.the_window = window
        self.param_section = param_ids[0]
        self.param_labels = param_ids[1]
        self.layout = QHBoxLayout(self)  # type: ignore

        self.label = QLabel(label)
        self.colorButton = ColorButton(color=initial_color)
        self.colorEdit = QLineEdit(initial_color)
        self.colorEdit.setFixedWidth(60)  # Half the length
        self.colorButton.colorChanged.connect(self.onColorChanged)
        self.colorEdit.textChanged.connect(self.onColorEditTextChanged)

        self.copyButton = QPushButton("Copy")
        self.pasteButton = QPushButton("Paste")
        self.copyButton.setFixedWidth(65)  # Shorter copy button
        self.pasteButton.setFixedWidth(65)  # Shorter paste button
        self.copyButton.clicked.connect(
            lambda: QApplication.clipboard().setText(self.colorEdit.text())  # type: ignore
        )
        self.pasteButton.clicked.connect(
            lambda: self.colorEdit.setText(QApplication.clipboard().text())  # type: ignore
        )
        self.setEnabled(activated_on_init)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.colorButton)
        self.layout.addWidget(self.colorEdit)
        self.layout.addWidget(self.copyButton)
        self.layout.addWidget(self.pasteButton)

    def onColorChanged(self, color):
        self.colorEdit.setText(color)
        rc = {label: color for label in self.param_labels}
        self.the_window.params[self.param_section].update(rc)
        self.the_window.updateFigure()

    def onColorEditTextChanged(self, text):
        if QColor(text).isValid():
            self.colorButton.setColor(text)
            param = {label: text for label in self.param_labels}
            self.the_window.params[self.param_section].update(param)
            self.the_window.updateFigure()

    def getValue(self):
        return self.colorButton._color


class Activator(QWidget):
    def __init__(
        self,
        window: QMainWindow,
        label,
        widget,
        param_ids=[],
        condition="",
    ):
        super(Activator, self).__init__()
        self.the_window = window
        self.widget = widget
        self.param_section = param_ids[0]
        self.param_label = param_ids[1]
        self.layout = QHBoxLayout(self)
        self.condition = condition

        self.checkbox = QCheckBox(label)
        self.checkbox.setChecked(
            self.the_window.params[self.param_section][self.param_label] == condition
        )
        self.checkbox.stateChanged.connect(self.onStateChanged)
        self.layout.addWidget(self.checkbox)

    def onStateChanged(self, state):
        self.widget.setEnabled(True if state != 2 else False)
        rc = {
            self.param_label: (self.condition if state == 2 else self.widget.getValue())
        }
        self.the_window.params[self.param_section].update(rc)
        self.the_window.updateFigure()


class Slider(QWidget):
    def __init__(
        self,
        window: QMainWindow,
        label,
        mini,
        maxi,
        tick_interval,
        param_ids=[],
        initial_value=0,
        activated_on_init=True,
    ):
        super(Slider, self).__init__()
        self.the_window = window
        self.param_section = param_ids[0]
        self.param_label = param_ids[1]

        self.label = QLabel(label)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(mini)
        self.slider.setMaximum(maxi)
        self.slider.setValue(initial_value * 2)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(tick_interval)
        self.slider.valueChanged.connect(self.onValueChanged)
        self.setEnabled(activated_on_init)

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.slider)

    def onValueChanged(self, value):
        rc = {self.param_label: value / 2}
        self.the_window.params[self.param_section].update(rc)
        self.the_window.updateFigure()

    def getValue(self):
        return self.slider.value() / 2


class Dropdown(QWidget):
    def __init__(
        self,
        window: QMainWindow,
        label,
        items=[],
        param_values=[],
        param_ids=[],
        initial_item=0,
        activated_on_init=True,
    ):
        super(Dropdown, self).__init__()
        self.the_window = window
        self.param_section = param_ids[0]
        self.param_label = param_ids[1]
        self.param_values = param_values

        self.label = QLabel(label)
        self.dropdown = QComboBox()
        self.dropdown.addItems(items)
        self.dropdown.setCurrentIndex(self.param_values.index(initial_item))
        self.dropdown.currentIndexChanged.connect(self.onCurrentIndexChanged)
        self.setEnabled(activated_on_init)

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.dropdown)

    def getValue(self):
        return self.dropdown.currentIndex()

    def onCurrentIndexChanged(self, index):
        rc = {self.param_label: self.param_values[index]}
        self.the_window.params[self.param_section].update(rc)
        self.the_window.updateFigure()


class GLCanvas(FigureCanvas):
    def __init__(self, params: dict, width=5, height=4):
        self.params = params
        self.gl_fig = gl.Figure(size=(width, height), figure_style="dark")
        self.compute_initial_figure()

        self.axes = self.gl_fig._axes
        self.fig = self.gl_fig._figure
        super(GLCanvas, self).__init__(self.fig)

    def compute_initial_figure(self):
        curve = gl.Curve([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
        curve.area_between(0, 2, True)
        # curve.add_errorbars(y_error=1)
        # curve2 = gl.Curve([0, 1, 2, 3, 4], [11, 2, 21, 4, 41]) + 1
        # curve3 = gl.Curve([0, 1, 2, 3, 4], [12, 3, 22, 5, 42]) + 2
        self.gl_fig.add_element(curve)  # , curve2, curve3)
        self.gl_fig._prepare_figure(default_params=self.params)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Updatable parameters
        self.params = gl.file_manager.FileLoader("plain").load()

        # Main widget and layout
        self.mainWidget = QWidget(self)
        self.mainLayout = QVBoxLayout(self.mainWidget)

        # Add a field for the figure style name
        self.figureStyleName = QLineEdit(self)
        self.figureStyleName.setText("new_thing!")
        self.figureStyleName.setFixedWidth(200)
        self.mainLayout.addWidget(self.figureStyleName)

        # Add save button
        self.saveButton = QPushButton("Save", self)
        self.saveButton.clicked.connect(self.save)
        self.saveButton.setFixedWidth(200)
        self.mainLayout.addWidget(self.saveButton)

        # Create a horizontal splitter to contain the tab widget and canvas
        self.splitter = QSplitter(Qt.Horizontal)  # type: ignore

        # Create and add the tab widget and canvas
        self.tabWidget = QTabWidget()
        self.canvas = GLCanvas(width=5, height=4, params=self.params)
        self.splitter.addWidget(self.tabWidget)
        self.splitter.addWidget(self.canvas)

        # Set the splitter as the main layout widget
        self.mainLayout.addWidget(self.splitter)

        # Combined Figure and Axes tab
        self.figureTab = QWidget()
        self.tabWidget.addTab(self.figureTab, "Figure")
        self.create_figure_tab()

        # 1D Plotting tab with nested tabs
        self.plotting1DTab = QWidget()
        self.tabWidget.addTab(self.plotting1DTab, "1D Plotting")
        self.create_plotting_1d_tab()

        # 2D Plotting tab with nested tabs
        self.plotting2DTab = QWidget()
        self.tabWidget.addTab(self.plotting2DTab, "2D Plotting")
        self.create_plotting_2d_tab()

        # Fits tab with nested tabs
        self.fitsTab = QWidget()
        self.tabWidget.addTab(self.fitsTab, "Fits")
        self.create_fits_tab()

        # Shapes tab with nested tabs
        self.shapesTab = QWidget()
        self.tabWidget.addTab(self.shapesTab, "Shapes")
        self.create_shapes_tab()

        # Other GL Objects tab with nested tabs
        self.otherGLTab = QWidget()
        self.tabWidget.addTab(self.otherGLTab, "Other GL Objects")
        self.create_other_gl_tab()

        # Set the main widget
        self.setCentralWidget(self.mainWidget)

    def create_figure_tab(self):
        self.figureTabLayout = QVBoxLayout()
        self.figureTabLayout.setAlignment(Qt.AlignTop)

        # Section for Colors
        self.colors_label = QLabel("Colors:")
        self.colors_label.setStyleSheet("font-weight: bold;")
        self.figureTabLayout.addWidget(self.colors_label)

        self.colors_line = QFrame()
        self.colors_line.setFrameShape(QFrame.HLine)
        self.colors_line.setFrameShadow(QFrame.Sunken)
        self.figureTabLayout.addWidget(self.colors_line)

        # figure face color
        self.figure_color_widget = ColorPickerWidget(
            self,
            label="Figure Color:",
            param_ids=["rc_params", ["figure.facecolor"]],
            initial_color=self.params["rc_params"]["figure.facecolor"],
        )
        self.figureTabLayout.addWidget(self.figure_color_widget)

        # axes face color
        self.axes_face_color_widget = ColorPickerWidget(
            self,
            label="Axes Face Color:",
            param_ids=["rc_params", ["axes.facecolor"]],
            initial_color=self.params["rc_params"]["axes.facecolor"],
        )
        self.figureTabLayout.addWidget(self.axes_face_color_widget)

        # axes edge color
        self.axes_edge_color_widget = ColorPickerWidget(
            self,
            label="Axes Edge Color:",
            param_ids=["rc_params", ["axes.edgecolor"]],
            initial_color=self.params["rc_params"]["axes.edgecolor"],
        )
        self.figureTabLayout.addWidget(self.axes_edge_color_widget)

        # ticks color
        self.axes_ticks_color_widget = ColorPickerWidget(
            self,
            label="Ticks Color:",
            param_ids=["rc_params", ["xtick.color", "ytick.color"]],
            initial_color=self.params["rc_params"]["xtick.color"],
        )
        self.figureTabLayout.addWidget(self.axes_ticks_color_widget)

        # Section for Grid
        self.grid_label = QLabel("Grid:")
        self.grid_label.setStyleSheet("font-weight: bold;")
        self.figureTabLayout.addWidget(self.grid_label)

        self.grid_line = QFrame()
        self.grid_line.setFrameShape(QFrame.HLine)
        self.grid_line.setFrameShadow(QFrame.Sunken)
        self.figureTabLayout.addWidget(self.grid_line)

        # grid color
        self.axes_grid_color_widget = ColorPickerWidget(
            self,
            label="Grid Color:",
            param_ids=["rc_params", ["grid.color"]],
            initial_color=self.params["rc_params"]["grid.color"],
        )
        self.figureTabLayout.addWidget(self.axes_grid_color_widget)

        # grid on/off
        self.axes_grid_on_button = QPushButton("Toggle Grid", self)
        self.axes_grid_on_button.clicked.connect(self.axes_grid_on_clicked)
        self.figureTabLayout.addWidget(self.axes_grid_on_button)

        # grid line width (use slider)
        self.axes_grid_line_width_label = QLabel("Grid Line Width:")
        self.figureTabLayout.addWidget(self.axes_grid_line_width_label)
        self.axes_grid_line_width_slider = QSlider(Qt.Horizontal)  # type: ignore
        self.axes_grid_line_width_slider.setMinimum(0)
        self.axes_grid_line_width_slider.setMaximum(20)
        default_grid_width = int(self.params["rc_params"]["grid.linewidth"] * 2)
        self.axes_grid_line_width_slider.setValue(default_grid_width)
        self.axes_grid_line_width_slider.setTickPosition(QSlider.TicksBelow)
        self.axes_grid_line_width_slider.setTickInterval(1)
        self.axes_grid_line_width_slider.valueChanged.connect(
            self.axes_grid_line_width_changed
        )
        self.figureTabLayout.addWidget(self.axes_grid_line_width_slider)

        # grid line style (use dropdown)
        self.axes_grid_line_style_label = QLabel("Grid Line Style:")
        self.figureTabLayout.addWidget(self.axes_grid_line_style_label)
        self.axes_grid_line_style_dropdown = QComboBox()
        self.axes_grid_line_style_dropdown.addItem("Solid")
        self.axes_grid_line_style_dropdown.addItem("Dashed")
        self.axes_grid_line_style_dropdown.addItem("Dotted")
        self.axes_grid_line_style_dropdown.addItem("Dash-Dot")
        default_grid_style = self.params["rc_params"]["grid.linestyle"]
        self.axes_grid_line_style_dropdown.setCurrentIndex(
            ["-", "--", ":", "-."].index(default_grid_style)
        )
        self.axes_grid_line_style_dropdown.currentIndexChanged.connect(
            self.axes_grid_line_style_changed
        )
        self.figureTabLayout.addWidget(self.axes_grid_line_style_dropdown)

        self.figureTab.setLayout(self.figureTabLayout)

    def create_plotting_1d_tab(self):
        layout = QVBoxLayout()
        tabWidget = QTabWidget()

        # Example stubs for each sub-tab
        self.curveTab = QWidget()
        tabWidget.addTab(self.curveTab, "Curve")
        scatterTab = QWidget()
        tabWidget.addTab(scatterTab, "Scatter")
        histogramTab = QWidget()
        tabWidget.addTab(histogramTab, "Histogram")

        # create the sub tabs
        self.create_curve_tab()

        layout.addWidget(tabWidget)
        self.plotting1DTab.setLayout(layout)

    def create_curve_tab(self):
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
            self,
            "Line Width:",
            0,
            20,
            1,
            ["Curve", "line_width"],
            self.params["Curve"]["line_width"],
        )
        layout.addWidget(line_width_slider)

        # create linestyle drop down menu
        line_style_dropdown = Dropdown(
            self,
            "Line Style:",
            ["Solid", "Dashed", "Dotted", "Dash-Dot"],
            ["-", "--", ":", "-."],
            ["Curve", "line_style"],
            self.params["Curve"]["line_style"],
        )
        layout.addWidget(line_style_dropdown)

        # create fill under color picker and "same as curve" checkbox
        initial_fill_under_color = (
            "#000000"
            if self.params["Curve"]["fill_under_color"] == "same as curve"
            else self.params["Curve"]["fill_under_color"]
        )
        fill_under_color = ColorPickerWidget(
            self,
            "Fill Under",
            initial_fill_under_color,
            param_ids=["Curve", "fill_under_color"],
            activated_on_init=False,
        )
        fill_under_color_checkbox = Activator(
            self,
            "Same as curve",
            fill_under_color,
            ["Curve", "fill_under_color"],
            "same as curve",
        )
        layout.addWidget(fill_under_color)
        layout.addWidget(fill_under_color_checkbox)

        # create line cap style dropdown
        line_cap_style_dropdown = Dropdown(
            self,
            "Line Cap Style:",
            ["Squared", "Rounded", "Squared extended"],
            ["butt", "round", "projecting"],
            ["rc_params", "lines.solid_capstyle"],
            self.params["rc_params"]["lines.solid_capstyle"],
        )
        layout.addWidget(line_cap_style_dropdown)

        # create dash cap style dropdown
        dash_cap_style_dropdown = Dropdown(
            self,
            "Dash Cap Style:",
            ["Squared", "Rounded", "Squared extended"],
            ["butt", "round", "projecting"],
            ["rc_params", "lines.dash_capstyle"],
            self.params["rc_params"]["lines.dash_capstyle"],
        )
        layout.addWidget(dash_cap_style_dropdown)

        # create dashed join style dropdown
        dash_join_style_dropdown = Dropdown(
            self,
            "Dash Join Style:",
            ["Squared", "Rounded", "Beveled"],
            ["miter", "round", "bevel"],
            ["rc_params", "lines.dash_joinstyle"],
            self.params["rc_params"]["lines.dash_joinstyle"],
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
        cap_width_label = QLabel("Cap Width:")
        layout.addWidget(cap_width_label)
        cap_width_slider = Slider(self, "Cap Width:", 0, 20, 1, ["Curve", "cap_width"])
        layout.addWidget(cap_width_slider)

        # create errorbar color button and "same as curve" checkbox
        errorbars_initial_color = (
            "#000000"
            if self.params["Curve"]["errorbars_color"] == "same as curve"
            else self.params["Curve"]["errorbars_color"]
        )
        errorbars_color = ColorPickerWidget(
            self,
            "Color",
            errorbars_initial_color,
            ["Curve", ["errorbars_color"]],
            activated_on_init=self.params["Curve"]["errorbars_color"]
            != "same as curve",
        )
        errorbars_color_checkbox = Activator(
            self,
            "Same as curve",
            errorbars_color,
            param_ids=["Curve", "errorbars_color"],
            condition="same as curve",
        )
        layout.addWidget(errorbars_color)
        layout.addWidget(errorbars_color_checkbox)

        # create errorbars line width slider and "same as curve" checkbox
        initial_errorbars_line_width = (
            self.params["Curve"]["line_width"]
            if self.params["Curve"]["errorbars_line_width"] == "same as curve"
            else self.params["Curve"]["errorbars_line_width"]
        )
        errorbars_line_width_slider = Slider(
            self,
            "Line Width:",
            0,
            20,
            1,
            ["Curve", "errorbars_line_width"],
            initial_errorbars_line_width,
            activated_on_init=self.params["Curve"]["errorbars_line_width"]
            != "same as curve",
        )
        errorbars_line_width_checkbox = Activator(
            self,
            "Same as curve",
            errorbars_line_width_slider,
            param_ids=["Curve", "errorbars_line_width"],
            condition="same as curve",
        )
        layout.addWidget(errorbars_line_width_slider)
        layout.addWidget(errorbars_line_width_checkbox)

        # create errorbars cap thickness slider and "same as curve" checkbox
        initial_cap_thickness = (
            self.params["Curve"]["line_width"]
            if self.params["Curve"]["cap_thickness"] == "same as curve"
            else self.params["Curve"]["cap_thickness"]
        )
        cap_thickness_slider = Slider(
            self,
            "Cap Thickness:",
            0,
            20,
            1,
            ["Curve", "cap_thickness"],
            initial_cap_thickness,
            activated_on_init=self.params["Curve"]["cap_thickness"] != "same as curve",
        )
        cap_thickness_checkbox = Activator(
            self,
            "Same as curve",
            cap_thickness_slider,
            ["Curve", "cap_thickness"],
            "same as curve",
        )
        layout.addWidget(cap_thickness_slider)
        layout.addWidget(cap_thickness_checkbox)

        # add layout to tab widget
        self.curveTab.setLayout(layout)

    def create_plotting_2d_tab(self):
        layout = QVBoxLayout()
        tabWidget = QTabWidget()

        # Example stubs for each sub-tab
        contourTab = QWidget()
        tabWidget.addTab(contourTab, "Contour")
        heatmapTab = QWidget()
        tabWidget.addTab(heatmapTab, "Heatmap")
        streamTab = QWidget()
        tabWidget.addTab(streamTab, "Stream")
        vectorFieldTab = QWidget()
        tabWidget.addTab(vectorFieldTab, "VectorField")

        layout.addWidget(tabWidget)
        self.plotting2DTab.setLayout(layout)

    def create_fits_tab(self):
        layout = QVBoxLayout()
        tabWidget = QTabWidget()

        fitFromPolynomialTab = QWidget()
        tabWidget.addTab(fitFromPolynomialTab, "Polynomial")
        fitFromSineTab = QWidget()
        tabWidget.addTab(fitFromSineTab, "Sine")
        fitFromExponentialTab = QWidget()
        tabWidget.addTab(fitFromExponentialTab, "Exponential")
        fitFromGaussianTab = QWidget()
        tabWidget.addTab(fitFromGaussianTab, "Gaussian")
        fitFromLogTab = QWidget()
        tabWidget.addTab(fitFromLogTab, "Log")
        fitFromSquareRootTab = QWidget()
        tabWidget.addTab(fitFromSquareRootTab, "Square Root")
        fitFromFunctionTab = QWidget()
        tabWidget.addTab(fitFromFunctionTab, "Function")

        layout.addWidget(tabWidget)
        self.fitsTab.setLayout(layout)

    def create_shapes_tab(self):
        layout = QVBoxLayout()
        tabWidget = QTabWidget()

        # Example stubs for each sub-tab
        circleTab = QWidget()
        tabWidget.addTab(circleTab, "Circle")
        rectangleTab = QWidget()
        tabWidget.addTab(rectangleTab, "Rectangle")
        arrowTab = QWidget()
        tabWidget.addTab(arrowTab, "Arrow")
        lineTab = QWidget()
        tabWidget.addTab(lineTab, "Line")

        layout.addWidget(tabWidget)
        self.shapesTab.setLayout(layout)

    def create_other_gl_tab(self):
        layout = QVBoxLayout()
        tabWidget = QTabWidget()

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
        self.otherGLTab.setLayout(layout)

    def axes_grid_on_clicked(self):
        rc = {"axes.grid": not self.params["rc_params"].get("axes.grid", False)}
        self.params["rc_params"].update(rc)
        self.updateFigure()

    def axes_grid_line_width_changed(self, value):
        rc = {"grid.linewidth": value / 2}
        self.params["rc_params"].update(rc)
        self.updateFigure()

    def axes_grid_line_style_changed(self, value):
        rc = {"grid.linestyle": ["-", "--", ":", "-."][value]}
        self.params["rc_params"].update(rc)
        self.updateFigure()

    def line_width_changed(self, value):
        rc = {"line_width": value / 2}
        self.params["Curve"].update(rc)
        self.updateFigure()

    def line_style_changed(self, value):
        rc = {"line_style": ["-", "--", ":", "-."][value]}
        self.params["Curve"].update(rc)
        self.updateFigure()

    def cap_width_changed(self, value):
        rc = {"cap_width": value / 2}
        self.params["Curve"].update(rc)
        self.updateFigure()

    def errorbars_color_checkbox_changed(self, value):
        if value == 2:
            rc = {"errorbars_color": "same as curve"}
            self.params["Curve"].update(rc)
            self.updateFigure()
        else:
            pass

    def errorbars_line_width_changed(self, value):
        rc = {"errorbars_line_width": value / 2}
        self.params["Curve"].update(rc)
        self.updateFigure()

    def cap_thickness_changed(self, value):
        rc = {"cap_thickness": value / 2}
        self.params["Curve"].update(rc)
        self.updateFigure()

    def updateFigure(self):
        # self.canvas.deleteLater()
        close()
        canvas = GLCanvas(width=5, height=4, params=self.params)
        self.splitter.replaceWidget(1, canvas)
        self.canvas = canvas

    def save(self):
        # get the figure style name
        name = self.figureStyleName.text()
        gl.file_manager.FileSaver(name, self.params).save()


app = QApplication(sys.argv)
mainWin = MainWindow()
mainWin.show()
sys.exit(app.exec_())
