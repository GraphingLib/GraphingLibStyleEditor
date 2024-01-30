import sys

import graphinglib as gl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication,
    QColorDialog,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSlider,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


class ColorButton(QtWidgets.QPushButton):
    colorChanged = pyqtSignal(str)

    def __init__(self, *args, color=None, **kwargs):
        super(ColorButton, self).__init__(*args, **kwargs)
        self._color = None
        self._default = color
        self.pressed.connect(self.onColorPicker)
        self.setColor(self._default)
        self.setFixedSize(30, 30)  # Smaller color button

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
        dlg = QtWidgets.QColorDialog(self)
        if self._color:
            dlg.setCurrentColor(QtGui.QColor(self._color))

        # Calculate the position to move the dialog next to the button
        button_pos = self.mapToGlobal(self.pos())
        dlg.move(button_pos.x(), button_pos.y())

        if dlg.exec_():
            self.setColor(dlg.currentColor().name())

    def mousePressEvent(self, e):
        if e.button() == Qt.RightButton:  # type: ignore
            self.setColor(self._default)
        return super(ColorButton, self).mousePressEvent(e)


class ColorPickerWidget(QtWidgets.QWidget):
    def __init__(
        self,
        window: QMainWindow,
        label="Pick a colour:",
        initial_color="#ff0000",
        rc_label=[],
    ):
        super().__init__()
        self.the_window = window
        self.rc_label = rc_label
        self.layout = QtWidgets.QHBoxLayout(self)  # type: ignore

        self.label = QtWidgets.QLabel(label)
        self.colorButton = ColorButton(color=initial_color)
        self.colorEdit = QtWidgets.QLineEdit(initial_color)
        self.colorEdit.setFixedWidth(60)  # Half the length
        self.colorButton.colorChanged.connect(self.onColorChanged)
        self.colorEdit.textChanged.connect(self.onColorEditTextChanged)

        self.copyButton = QtWidgets.QPushButton("C")
        self.pasteButton = QtWidgets.QPushButton("V")
        self.copyButton.setFixedWidth(40)  # Shorter copy button
        self.pasteButton.setFixedWidth(40)  # Shorter paste button
        self.copyButton.clicked.connect(
            lambda: QtWidgets.QApplication.clipboard().setText(self.colorEdit.text())  # type: ignore
        )
        self.pasteButton.clicked.connect(
            lambda: self.colorEdit.setText(QtWidgets.QApplication.clipboard().text())  # type: ignore
        )

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.colorButton)
        self.layout.addWidget(self.colorEdit)
        self.layout.addWidget(self.copyButton)
        self.layout.addWidget(self.pasteButton)

    def onColorChanged(self, color):
        self.colorEdit.setText(color)
        rc = {label: color for label in self.rc_label}
        self.the_window.rc.update(rc)
        self.the_window.updateFigure()

    def onColorEditTextChanged(self, text):
        if QtGui.QColor(text).isValid():
            self.colorButton.setColor(text)
            rc = {label: text for label in self.rc_label}
            self.the_window.rc.update(rc)
            self.the_window.updateFigure()


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = plt.figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        self.compute_initial_figure()
        super(MplCanvas, self).__init__(self.fig)

    def compute_initial_figure(self):
        # Example plot; replace with your actual plotting code
        self.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])


class GLCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100, rc=None):
        self.gl_fig = gl.Figure(size=(width, height), figure_style="dark")
        if rc is not None:
            self.gl_fig.update_rc_params(rc)
        self.compute_initial_figure()

        self.axes = self.gl_fig._axes
        self.fig = self.gl_fig._figure
        super(GLCanvas, self).__init__(self.fig)

    def compute_initial_figure(self):
        # Example plot; replace with your actual plotting code
        curve = gl.Curve([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
        self.gl_fig.add_element(curve)
        self.gl_fig._prepare_figure()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Main widget and layout
        self.mainWidget = QWidget(self)
        self.mainLayout = QHBoxLayout(self.mainWidget)

        # Tab widget for parameters
        self.tabWidget = QTabWidget()
        self.mainLayout.addWidget(self.tabWidget)

        # Tabs for different settings
        self.figureTab = QWidget()
        self.axesTab = QWidget()
        self.curveTab = QWidget()
        self.scatterTab = QWidget()

        self.tabWidget.addTab(self.figureTab, "Figure")
        self.tabWidget.addTab(self.axesTab, "Axes")
        self.tabWidget.addTab(self.curveTab, "Curve")
        self.tabWidget.addTab(self.scatterTab, "Scatter")

        # Create layouts for each tab
        self.create_figure_tab()
        self.create_axes_tab()
        self.create_curve_tab()
        self.create_scatter_tab()

        # Matplotlib canvas
        self.canvas = GLCanvas(self, width=5, height=4, dpi=100)
        self.mainLayout.addWidget(self.canvas)

        # Set the main widget
        self.setCentralWidget(self.mainWidget)

        # User updateable rc params
        self.rc = {}

    def create_figure_tab(self):
        self.figureTabLayout = QVBoxLayout()
        # figure face color
        self.figure_color_widget = ColorPickerWidget(
            self,
            label="Figure Color:",
            rc_label=["figure.facecolor"],
            initial_color=plt.rcParams.get("figure.facecolor", "#ffffff"),
        )
        self.figureTabLayout.addWidget(self.figure_color_widget)
        self.figureTab.setLayout(self.figureTabLayout)

    def create_axes_tab(self):
        self.axesTabLayout = QVBoxLayout()

        # Section for Colors
        self.colors_label = QLabel("Colors:")
        self.colors_label.setStyleSheet("font-weight: bold;")
        self.axesTabLayout.addWidget(self.colors_label)

        self.colors_line = QFrame()
        self.colors_line.setFrameShape(QFrame.HLine)
        self.colors_line.setFrameShadow(QFrame.Sunken)
        self.axesTabLayout.addWidget(self.colors_line)

        # axes face color
        self.axes_face_color_widget = ColorPickerWidget(
            self,
            label="Axes Face Color:",
            rc_label=["axes.facecolor"],
            initial_color=plt.rcParams.get("axes.facecolor", "#ffffff"),
        )
        self.axesTabLayout.addWidget(self.axes_face_color_widget)

        # axes edge color
        self.axes_edge_color_widget = ColorPickerWidget(
            self,
            label="Axes Edge Color:",
            rc_label=["axes.edgecolor"],
            initial_color=plt.rcParams.get("axes.edgecolor", "#000000"),
        )
        self.axesTabLayout.addWidget(self.axes_edge_color_widget)

        # ticks color
        self.axes_ticks_color_widget = ColorPickerWidget(
            self,
            label="Ticks Color:",
            rc_label=["xtick.color", "ytick.color"],
            initial_color=plt.rcParams.get("xtick.color", "#000000"),
        )
        self.axesTabLayout.addWidget(self.axes_ticks_color_widget)

        # Section for Grid
        self.grid_label = QLabel("Grid:")
        self.grid_label.setStyleSheet("font-weight: bold;")
        self.axesTabLayout.addWidget(self.grid_label)

        self.grid_line = QFrame()
        self.grid_line.setFrameShape(QFrame.HLine)
        self.grid_line.setFrameShadow(QFrame.Sunken)
        self.axesTabLayout.addWidget(self.grid_line)

        # grid color
        self.axes_grid_color_widget = ColorPickerWidget(
            self,
            label="Grid Color:",
            rc_label=["grid.color"],
            initial_color=plt.rcParams.get("grid.color", "#000000"),
        )
        self.axesTabLayout.addWidget(self.axes_grid_color_widget)

        # grid on/off
        self.axes_grid_on_button = QPushButton("Toggle Grid", self)
        self.axes_grid_on_button.clicked.connect(self.axes_grid_on_clicked)
        self.axesTabLayout.addWidget(self.axes_grid_on_button)

        # grid line width (use slider)
        self.axes_grid_line_width_label = QLabel("Grid Line Width:")
        self.axesTabLayout.addWidget(self.axes_grid_line_width_label)
        self.axes_grid_line_width_slider = QSlider(Qt.Horizontal)  # type: ignore
        self.axes_grid_line_width_slider.setMinimum(0)
        self.axes_grid_line_width_slider.setMaximum(20)
        self.axes_grid_line_width_slider.setValue(1)
        self.axes_grid_line_width_slider.setTickPosition(QSlider.TicksBelow)
        self.axes_grid_line_width_slider.setTickInterval(1)
        self.axes_grid_line_width_slider.valueChanged.connect(
            self.axes_grid_line_width_changed
        )
        self.axesTabLayout.addWidget(self.axes_grid_line_width_slider)

        # grid line style (use dropdown)
        self.axes_grid_line_style_label = QLabel("Grid Line Style:")
        self.axesTabLayout.addWidget(self.axes_grid_line_style_label)
        self.axes_grid_line_style_dropdown = QComboBox()
        self.axes_grid_line_style_dropdown.addItem("Solid")
        self.axes_grid_line_style_dropdown.addItem("Dashed")
        self.axes_grid_line_style_dropdown.addItem("Dotted")
        self.axes_grid_line_style_dropdown.addItem("Dash-Dot")
        self.axes_grid_line_style_dropdown.currentIndexChanged.connect(
            self.axes_grid_line_style_changed
        )
        self.axesTabLayout.addWidget(self.axes_grid_line_style_dropdown)

        self.axesTab.setLayout(self.axesTabLayout)

    def create_curve_tab(self):
        self.curveTabLayout = QVBoxLayout()
        self.curveTabLayout.addWidget(QLabel("Curve settings will go here"))
        self.curveTab.setLayout(self.curveTabLayout)

    def create_scatter_tab(self):
        self.scatterTabLayout = QVBoxLayout()
        self.scatterTabLayout.addWidget(QLabel("Scatter settings will go here"))
        self.scatterTab.setLayout(self.scatterTabLayout)

    def figure_color_clicked(self):
        color = QColorDialog.getColor()
        if color.isValid():
            rc = {"figure.facecolor": color.name()}
            self.rc.update(rc)
            self.updateFigure()

    def axes_face_color_clicked(self):
        color = QColorDialog.getColor()
        if color.isValid():
            rc = {"axes.facecolor": color.name()}
            self.rc.update(rc)
            self.updateFigure()

    def axes_edge_color_clicked(self):
        color = QColorDialog.getColor()
        if color.isValid():
            rc = {"axes.edgecolor": color.name()}
            self.rc.update(rc)
            self.updateFigure()

    def axes_ticks_color_clicked(self):
        color = QColorDialog.getColor()
        if color.isValid():
            rc = {"xtick.color": color.name(), "ytick.color": color.name()}
            self.rc.update(rc)
            self.updateFigure()

    def axes_grid_color_clicked(self):
        color = QColorDialog.getColor()
        if color.isValid():
            rc = {"grid.color": color.name()}
            self.rc.update(rc)
            self.updateFigure()

    def axes_grid_on_clicked(self):
        rc = {"axes.grid": not self.rc.get("axes.grid", False)}
        self.rc.update(rc)
        self.updateFigure()

    def axes_grid_line_width_changed(self, value):
        rc = {"grid.linewidth": value / 2}
        self.rc.update(rc)
        self.updateFigure()

    def axes_grid_line_style_changed(self, value):
        rc = {"grid.linestyle": ["-", "--", ":", "-."][value]}
        self.rc.update(rc)
        self.updateFigure()

    def updateFigure(self):
        # Re-create the canvas
        self.mainLayout.removeWidget(self.canvas)
        self.canvas.deleteLater()
        plt.close()
        # self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.canvas = GLCanvas(self, width=5, height=4, dpi=100, rc=self.rc)
        self.mainLayout.addWidget(self.canvas)


app = QApplication(sys.argv)
mainWin = MainWindow()
mainWin.show()
sys.exit(app.exec_())
