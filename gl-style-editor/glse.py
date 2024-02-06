import sys

import graphinglib as gl
from matplotlib.pyplot import close
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSplitter,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from .plotting_1d_tab import create_plotting_1d_tab
from .plotting_2d_tab import create_plotting_2d_tab
from .figure_tab import create_figure_tab
from .fits_tab import create_fits_tab
from .shapes_tab import create_shapes_tab
from .other_gl_tab import create_other_gl_tab


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
        curve.get_area_between(0, 2, True)
        curve.add_errorbars(y_error=1)
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
        create_figure_tab(self)

        # 1D Plotting tab with nested tabs
        self.plotting1DTab = QWidget()
        self.tabWidget.addTab(self.plotting1DTab, "1D Plotting")
        create_plotting_1d_tab(self)

        # 2D Plotting tab with nested tabs
        self.plotting2DTab = QWidget()
        self.tabWidget.addTab(self.plotting2DTab, "2D Plotting")
        create_plotting_2d_tab(self)

        # Fits tab with nested tabs
        self.fitsTab = QWidget()
        self.tabWidget.addTab(self.fitsTab, "Fits")
        create_fits_tab(self)

        # Shapes tab with nested tabs
        self.shapesTab = QWidget()
        self.tabWidget.addTab(self.shapesTab, "Shapes")
        create_shapes_tab(self)

        # Other GL Objects tab with nested tabs
        self.otherGLTab = QWidget()
        self.tabWidget.addTab(self.otherGLTab, "Other GL Objects")
        create_other_gl_tab(self)

        # Set the main widget
        self.setCentralWidget(self.mainWidget)

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


def run():
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
