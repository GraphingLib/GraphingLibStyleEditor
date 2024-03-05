import sys

import graphinglib as gl
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.pyplot import close
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QSplitter,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from .figure_tab import create_figure_tab
from .fits_tab import create_fits_tab
from .other_gl_tab import create_other_gl_tab
from .plotting_1d_tab import create_plotting_1d_tab
from .plotting_2d_tab import create_plotting_2d_tab
from .shapes_tab import create_shapes_tab


class GLCanvas(FigureCanvas):
    def __init__(self, params: dict, width=5, height=4):
        self.params = params
        self.gl_fig = gl.Figure(size=(width, height), figure_style="dark")
        self.compute_initial_figure()

        self.axes = self.gl_fig._axes
        self.fig = self.gl_fig._figure
        super(GLCanvas, self).__init__(self.fig)

    def compute_initial_figure(self):
        # curve = gl.Curve([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
        # # curve.add_errorbars(y_error=2)
        # curve2 = gl.Curve([0, 1, 2, 3, 4], [11, 2, 21, 4, 41]) + 1
        # curve3 = gl.Curve([0, 1, 2, 3, 4], [12, 3, 22, 5, 42]) + 2
        # self.gl_fig.add_elements(curve, curve2, curve3)
        # self.gl_fig._prepare_figure(default_params=self.params)
        # contour = gl.Contour.from_function(
        #     lambda x, y: np.sin(x) + np.cos(y), (-10, 10), (-10, 10)
        # )
        # self.gl_fig.add_elements(contour)
        # circle = gl.Circle(0, 0, 5)
        # rect = gl.Rectangle(0, 0, 5, 5)
        # self.gl_fig.add_elements(circle, rect)
        # self.gl_fig._prepare_figure(default_params=self.params)
        # color = self.params["Circle"]["color"]
        # heatmap = gl.Heatmap.from_function(
        #     lambda x, y: np.sin(x) + np.cos(y - 1),
        #     (0, 10),
        #     (0, 10),
        # )
        # self.gl_fig.add_elements(heatmap)
        # self.gl_fig._prepare_figure(default_params=self.params)
        x_grid, y_grid = np.meshgrid(np.linspace(0, 11, 30), np.linspace(0, 11, 30))
        u, v = (np.cos(x_grid * 0.2), np.sin(y_grid * 0.3))

        stream = gl.Stream(x_grid, y_grid, u, v)
        point = gl.Point(5, 5)
        self.gl_fig.add_elements(stream, point)
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
        figureTabLayout = create_figure_tab(self)
        self.figureTab.setLayout(figureTabLayout)
        self.figureTabScrollArea = QScrollArea()
        self.figureTabScrollArea.setWidgetResizable(True)
        self.figureTabScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.figureTabScrollArea.setWidget(self.figureTab)
        self.tabWidget.addTab(self.figureTabScrollArea, "Figure")

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
