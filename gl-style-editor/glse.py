import re
import sys

import graphinglib as gl
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.pyplot import close
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent, QKeySequence
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QShortcut,
    QSplitter,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)
from qt_material import apply_stylesheet

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
        curve = gl.Curve([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
        # curve.add_errorbars(y_error=2)
        curve2 = gl.Curve([0, 1, 2, 3, 4], [11, 2, 21, 4, 41]) + 1
        curve3 = gl.Curve([0, 1, 2, 3, 4], [12, 3, 22, 5, 42]) + 2
        self.gl_fig.add_elements(curve, curve2, curve3)
        self.gl_fig._prepare_figure(default_params=self.params)
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
        # x_grid, y_grid = np.meshgrid(np.linspace(0, 11, 30), np.linspace(0, 11, 30))
        # u, v = (np.cos(x_grid * 0.2), np.sin(y_grid * 0.3))

        # stream = gl.Stream(x_grid, y_grid, u, v)
        # point = gl.Point(5, 5)
        # text = gl.Text(7, 7, "Hello World!")
        # self.gl_fig.add_elements(stream, point, text)
        # self.gl_fig._prepare_figure(default_params=self.params)
        # data = [
        #     [5, 223.9369, 0.0323, 0.0532, 0.1764],
        #     [10, 223.9367, 0.0324, 0.0533, 0.1765],
        #     [15, 223.9367, 0.0325, 0.0534, 0.1764],
        #     [20, 223.9387, 0.0326, 0.0535, 0.1763],
        #     [25, 223.9385, 0.0327, 0.0536, 0.1761],
        # ]
        # columns = [
        #     "Time (s)",
        #     "Voltage (V)",
        #     "Current 1 (A)",
        #     "Current 2 (A)",
        #     "Current 3 (A)",
        # ]
        # rows = ["Series 1", "Series 2", "Series 3", "Series 4", "Series 5"]
        # colors = ["#bfbfbf"] * 5
        # table = gl.Table(
        #     cell_text=data,
        #     col_labels=columns,
        #     row_labels=rows,
        #     row_colors=colors,
        #     col_colors=colors,
        #     location="center",
        # )
        # self.gl_fig.add_elements(table)
        # self.gl_fig._prepare_figure(default_params=self.params)
        # hlines = gl.Hlines(y=[1, 2, 3], x_min=0, x_max=10)
        # vlines = gl.Vlines(x=[1, 2, 3], y_min=0, y_max=10)
        # self.gl_fig.add_elements(hlines, vlines)
        # self.gl_fig._prepare_figure(default_params=self.params)


class StyleManager(QDialog):
    def __init__(self, parent=None):
        super(StyleManager, self).__init__(parent)
        self.setWindowTitle("Manage Styles")
        self.setGeometry(100, 100, 200, 200)
        layout = QHBoxLayout()
        # Add list of styles to select from
        self.styles = gl.get_styles(gl=True)
        self.styles = list(dict.fromkeys(self.styles))
        self.styles = [s for s in self.styles if s]

        self.styleList = QListWidget()
        self.styleList.addItems(self.styles)
        # Limit to one selection
        self.styleList.setSelectionMode(QListWidget.SingleSelection)
        self.current_selection = None
        self.styleList.itemSelectionChanged.connect(self.update_selection)
        layout.addWidget(self.styleList)

        # Add vertical layout for buttons
        buttonLayout = QVBoxLayout()
        layout.addLayout(buttonLayout)

        # Add buttons to delete, rename styles, and set a style as the default
        self.renameButton = QPushButton("Rename", self)
        self.renameButton.clicked.connect(self.rename_style)
        self.deleteButton = QPushButton("Delete", self)
        self.deleteButton.clicked.connect(self.delete_style)
        self.duplicateButton = QPushButton("Duplicate", self)
        self.duplicateButton.clicked.connect(self.duplicate_style)
        self.defaultButton = QPushButton("Set as default", self)
        self.defaultButton.clicked.connect(self.set_default_style)

        buttonLayout.addWidget(self.renameButton)
        buttonLayout.addWidget(self.deleteButton)
        buttonLayout.addWidget(self.duplicateButton)
        buttonLayout.addWidget(self.defaultButton)

        self.setLayout(layout)

        self.shortcut_close = QShortcut(QKeySequence("Ctrl+W"), self)
        self.shortcut_close.activated.connect(self.close)

    def update_selection(self):
        self.current_selection = self.styleList.currentItem().text()

    def delete_style(self):
        if not self.current_selection:
            return
        # check if the current selection is in custom styles
        if self.current_selection not in gl.get_styles(gl=False):
            msg = "You can only delete custom styles. This style is built-in and cannot be deleted."
            QMessageBox.information(self, "Invalid Selection", msg)
            return

        if self.current_selection:
            msg = f"Are you sure you want to delete the style {self.current_selection}?"
            reply = QMessageBox.question(
                self, "Delete Style", msg, QMessageBox.Yes, QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                gl.file_manager.FileDeleter(self.current_selection).delete()
                self.styleList.clear()
                self.styles = gl.get_styles(gl=True)
                self.styles = list(dict.fromkeys(self.styles))
                self.styles = [s for s in self.styles if s]
                self.styleList.addItems(self.styles)
                self.current_selection = None

    def rename_style(self):
        if not self.current_selection:
            return
        # check if the current selection is in custom styles
        if self.current_selection not in gl.get_styles(gl=False):
            msg = "You can only rename custom styles. If you want to rename a built-in style, you can duplicate it."
            QMessageBox.information(self, "Invalid Selection", msg)
            return

        bad_name = True
        while bad_name:
            name, ok = QInputDialog.getText(
                self,
                "Rename Style",
                "Enter a new style name:",
                QLineEdit.Normal,
                "",
            )
            if ok and " " in name:
                msg = "Style names cannot contain spaces. Please enter a new name."
                QMessageBox.information(self, "Invalid Name", msg)
            elif ok and name in self.styles:
                msg = "This style already exists. Please enter a new name."
                QMessageBox.information(self, "Invalid Name", msg)
            else:
                bad_name = False
        if ok:
            # get the params of the current style
            params = gl.file_manager.FileLoader(self.current_selection).load()
            # save the params with the new name
            gl.file_manager.FileSaver(name, params).save()
            # delete the old style
            gl.file_manager.FileDeleter(self.current_selection).delete()
            # update the list of styles
            self.styleList.clear()
            self.styles = gl.get_styles(gl=True)
            self.styles = list(dict.fromkeys(self.styles))
            self.styles = [s for s in self.styles if s]
            self.styleList.addItems(self.styles)
            self.current_selection = None

    def duplicate_style(self):
        if not self.current_selection:
            return
        bad_name = True
        while bad_name:
            name, ok = QInputDialog.getText(
                self,
                "Duplicate Style",
                "Enter a new style name:",
                QLineEdit.Normal,
                "",
            )
            if ok and " " in name:
                msg = "Style names cannot contain spaces. Please enter a new name."
                QMessageBox.information(self, "Invalid Name", msg)
            elif ok and name in self.styles:
                msg = "This style already exists. Please enter a new name."
                QMessageBox.information(self, "Invalid Name", msg)
            else:
                bad_name = False

        if ok:
            if name in self.styles:
                msg = "This style already exists. Please enter a new name."
                QMessageBox.information(self, "Invalid Name", msg)
            else:
                params = gl.file_manager.FileLoader(self.current_selection).load()
                gl.file_manager.FileSaver(name, params).save()
                self.styleList.clear()
                self.styles = gl.get_styles(gl=True)
                self.styles = list(dict.fromkeys(self.styles))
                self.styles = [s for s in self.styles if s]
                self.styleList.addItems(self.styles)
                self.current_selection = None

    def set_default_style(self):
        if not self.current_selection:
            return
        msg = (
            "Setting a new default style will rename the current default style to 'plain'.\n"
            "Do you want to rename the current 'plain' style to something else or delete it?"
        )
        # Create a dialog with three buttons: "Rename", "Delete" and "Cancel"
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Set Default Style")
        dialog.setText(msg)
        rename_button = dialog.addButton("Rename", QMessageBox.ActionRole)
        delete_button = dialog.addButton("Delete", QMessageBox.ActionRole)
        cancel_button = dialog.addButton(QMessageBox.Cancel)
        dialog.setDefaultButton(QMessageBox.Cancel)
        reply = dialog.exec_()

        if reply == 0:
            dialog.close()
            style_to_make_plain = self.current_selection
            self.current_selection = "plain"
            self.rename_style()
            self.current_selection = style_to_make_plain
            params = gl.file_manager.FileLoader(self.current_selection).load()
            gl.file_manager.FileSaver("plain", params).save()
            gl.file_manager.FileDeleter(self.current_selection).delete()
            self.styleList.clear()
            self.styles = gl.get_styles(gl=True)
            self.styles = list(dict.fromkeys(self.styles))
            self.styles = [s for s in self.styles if s]
            self.styleList.addItems(self.styles)
            self.current_selection = None
        elif reply == 1:
            dialog.close()
            # delete the current "plain" style and rename the selected style to "plain"
            style_to_make_plain = self.current_selection
            self.current_selection = "plain"
            self.delete_style()
            self.current_selection = style_to_make_plain
            params = gl.file_manager.FileLoader(self.current_selection).load()
            gl.file_manager.FileSaver("plain", params).save()
            gl.file_manager.FileDeleter(self.current_selection).delete()
            self.styleList.clear()
            self.styles = gl.get_styles(gl=True)
            self.styles = list(dict.fromkeys(self.styles))
            self.styles = [s for s in self.styles if s]
            self.styleList.addItems(self.styles)
            self.current_selection = None
        else:
            return


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GraphingLib Style Editor")
        screen = self.screen()
        screen_size = screen.size()
        width = screen_size.width()
        height = screen_size.height()
        self.resize(int(width * 0.8), int(height * 0.6))

        # Updatable parameters
        self.current_style = "plain"
        self.unsaved_changes = {}
        self.params = gl.file_manager.FileLoader(self.current_style).load()
        self.original_params = {}
        for section in self.params:
            self.original_params[section] = {}
            for param in self.params[section]:
                self.original_params[section][param] = self.params[section][param]

        # Main widget and layout
        self.mainWidget = QWidget(self)
        self.mainLayout = QVBoxLayout(self.mainWidget)

        # Add menu bar
        self.menuBar = self.menuBar()
        self.fileMenu = self.menuBar.addMenu("File")

        # Add actions to the file menu
        self.newAction = self.fileMenu.addAction("New")
        self.openAction = self.fileMenu.addAction("Open")
        self.saveAction = self.fileMenu.addAction("Save")
        self.saveAsAction = self.fileMenu.addAction("Save As")
        self.managerAction = self.fileMenu.addAction("Manage styles...")

        self.saveAction.triggered.connect(self.save)
        self.saveAsAction.triggered.connect(self.save_as)
        self.openAction.triggered.connect(self.load)
        self.newAction.triggered.connect(self.new)
        self.managerAction.triggered.connect(self.manage_styles)

        # Connect key shortcuts to the file menu actions
        self.newAction.setShortcut("Ctrl+N")
        self.openAction.setShortcut("Ctrl+O")
        self.saveAction.setShortcut("Ctrl+S")
        self.managerAction.setShortcut("Ctrl+M")

        # Add a field for the figure style name
        self.upperLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.upperLayout)

        # Display the name of the current style with a label
        self.styleNameLabel = QLabel(self)
        self.styleNameLabel.setText("Current Style: " + self.current_style)
        self.styleNameLabel.setFixedWidth(250)
        self.styleNameLabel.setWordWrap(True)
        # add button to view unsaved changes
        self.viewUnsavedButton = QPushButton("View Unsaved Changes", self)
        self.viewUnsavedButton.clicked.connect(self.view_unsaved_changes)
        self.viewUnsavedButton.setFixedWidth(200)

        self.upperLayout.addWidget(self.styleNameLabel)
        self.upperLayout.addWidget(self.viewUnsavedButton)

        # Create a horizontal splitter to contain the tab widget and canvas
        self.splitter = QSplitter(Qt.Horizontal)  # type: ignore

        # Create and add the tab widget and canvas
        self.tabWidget = QTabWidget()
        self.canvas = GLCanvas(width=5, height=4, params=self.params)
        self.splitter.addWidget(self.tabWidget)
        self.splitter.addWidget(self.canvas)
        self.splitter.setSizes([int(width * 0.3), int(width * 0.3)])

        # Set the splitter as the main layout widget
        self.mainLayout.addWidget(self.splitter)

        # Create all the tabs
        self.create_tabs()

        # Set the main widget
        self.setCentralWidget(self.mainWidget)

    def create_tabs(self):
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

    def updateFigure(self):
        # self.canvas.deleteLater()
        close()
        canvas = GLCanvas(width=5, height=4, params=self.params)
        self.splitter.replaceWidget(1, canvas)
        self.canvas = canvas

    def load(self):
        if self.unsaved_changes:
            msg = "You have unsaved changes that will be lost. Are you sure you want to load a new style?"
            reply = QMessageBox.question(
                self, "Unsaved Changes", msg, QMessageBox.Yes, QMessageBox.No
            )
            if reply == QMessageBox.No:
                return
        # Make dialog to select style to load from list of styles
        styles = gl.get_styles(gl=True)
        styles = list(dict.fromkeys(styles))
        styles = [s for s in styles if s]
        style, ok = QInputDialog.getItem(
            self, "Load Style", "Select a style to load", styles, 0, False
        )
        if ok:
            # Load the style
            self.params = gl.file_manager.FileLoader(style).load()
            # update the current style
            self.current_style = style
            self.styleNameLabel.setText("Current Style: " + self.current_style)

            self.updateFigure()
            # Identify the current tab
            current_tab = self.tabWidget.currentIndex()
            try:
                current_sub_tab = (
                    self.tabWidget.currentWidget()
                    .layout()
                    .itemAt(0)
                    .widget()
                    .currentIndex()
                )
            except:
                current_sub_tab = None
            # remove all tabs and recreate them to update the params
            for i in range(self.tabWidget.count()):
                self.tabWidget.removeTab(0)
            self.create_tabs()
            # set the current tab
            self.tabWidget.setCurrentIndex(current_tab)
            if current_sub_tab is not None:
                self.tabWidget.currentWidget().layout().itemAt(
                    0
                ).widget().setCurrentIndex(current_sub_tab)
            # update the original params
            self.original_params = {}
            for section in self.params:
                self.original_params[section] = {}
                for param in self.params[section]:
                    self.original_params[section][param] = self.params[section][param]
            # clear unsaved changes
            self.unsaved_changes = {}

    def save(self):
        if self.current_style == "no name":
            self.save_as()
            return
        name = self.current_style
        gl.file_manager.FileSaver(name, self.params).save()

        # update the current style
        self.current_style = name
        self.styleNameLabel.setText("Current Style: " + self.current_style)

        # clear unsaved changes
        self.unsaved_changes = {}

        # update the original params
        self.original_params = {}
        for section in self.params:
            self.original_params[section] = {}
            for param in self.params[section]:
                self.original_params[section][param] = self.params[section][param]

    def save_as(self):
        # ask for a new style name
        bad_name = True
        while bad_name:
            name, ok = QInputDialog.getText(
                self, "Save As", "Enter a new style name:", QLineEdit.Normal, ""
            )
            if ok and " " in name:
                msg = "Style names cannot contain spaces. Please enter a new name."
                QMessageBox.information(self, "Invalid Name", msg)
            else:
                bad_name = False
        # if the user clicked ok
        if ok:
            # check if the name is already in use
            styles = gl.get_styles(gl=False)
            styles = list(dict.fromkeys(styles))
            styles = [s for s in styles if s]
            if name in styles:
                msg = "This style already exists. Do you want to overwrite it?"
                reply = QMessageBox.question(
                    self, "Overwrite Style", msg, QMessageBox.Yes, QMessageBox.No
                )
                if reply == QMessageBox.No:
                    return
            # save the style
            gl.file_manager.FileSaver(name, self.params).save()
            # update the current style
            self.current_style = name
            self.styleNameLabel.setText("Current Style: " + self.current_style)
            # clear unsaved changes
            self.unsaved_changes = {}
            # update the original params
            self.original_params = {}
            for section in self.params:
                self.original_params[section] = {}
                for param in self.params[section]:
                    self.original_params[section][param] = self.params[section][param]
        else:
            return

    def new(self):
        # check if there are unsaved changes
        if self.unsaved_changes:
            msg = "You have unsaved changes that will be lost. Are you sure you want to create a new style?"
            reply = QMessageBox.question(
                self, "Unsaved Changes", msg, QMessageBox.Yes, QMessageBox.No
            )
            if reply == QMessageBox.No:
                return

        # choose a style as a starting point
        styles = gl.get_styles(gl=True)
        styles = list(dict.fromkeys(styles))
        styles = [s for s in styles if s]
        style, ok = QInputDialog.getItem(
            self,
            "New Style",
            "Select a style to use as a starting point",
            styles,
            0,
            False,
        )
        if ok:
            # load the style
            self.params = gl.file_manager.FileLoader(style).load()
            # update the current style
            self.current_style = "no name"
            self.styleNameLabel.setText("Current Style: " + self.current_style)
            # update the figure
            self.updateFigure()
            # remove all tabs and recreate them to update the params
            for i in range(self.tabWidget.count()):
                self.tabWidget.removeTab(0)
            self.create_tabs()
            # update the original params
            self.original_params = {}
            for section in self.params:
                self.original_params[section] = {}
                for param in self.params[section]:
                    self.original_params[section][param] = self.params[section][param]
            # set unsaved changes to be the same as the original params
            for section in self.original_params:
                self.unsaved_changes[section] = {}
                for param in self.original_params[section]:
                    self.unsaved_changes[section][param] = self.original_params[
                        section
                    ][param]

    def manage_styles(self):
        # check if there are unsaved changes
        if self.unsaved_changes:
            msg = "You have unsaved changes which will be lost. Are you sure you want to manage styles?"
            reply = QMessageBox.question(
                self, "Unsaved Changes", msg, QMessageBox.Yes, QMessageBox.No
            )
            if reply == QMessageBox.No:
                return
        styleManager = StyleManager(self)
        styleManager.exec_()
        # reload the current style
        self.params = gl.file_manager.FileLoader(self.current_style).load()
        self.updateFigure()
        # remove all tabs and recreate them to update the params
        for i in range(self.tabWidget.count()):
            self.tabWidget.removeTab(0)
        self.create_tabs()
        # update the original params
        self.original_params = {}
        for section in self.params:
            self.original_params[section] = {}
            for param in self.params[section]:
                self.original_params[section][param] = self.params[section][param]
        # set unsaved changes to be nothing
        self.unsaved_changes = {}

        # update the style name label
        self.styleNameLabel.setText("Current Style: " + self.current_style)

    def update_params(self, section: str, params_name: str | list, value):
        if not isinstance(params_name, list):
            params_name = [params_name]
        for p in params_name:
            # Update the parameters
            self.params[section][p] = value

            # Check if the new value is different from the original
            orig = self.original_params[section][p]
            if orig != value:
                # set value in unsaved changes dict (may have to create section/params_name key)
                if section not in self.unsaved_changes:
                    self.unsaved_changes[section] = {}
                self.unsaved_changes[section][p] = value
            else:
                # remove value from unsaved changes dict
                if section in self.unsaved_changes:
                    if p in self.unsaved_changes[section]:
                        del self.unsaved_changes[section][p]
                    if not self.unsaved_changes[section]:
                        del self.unsaved_changes[section]

        # Update the figure
        self.updateFigure()

        # Update the style name label to indicate unsaved changes
        if self.unsaved_changes:
            self.styleNameLabel.setText(
                "Current Style: " + self.current_style + " (unsaved changes)"
            )
        else:
            self.styleNameLabel.setText("Current Style: " + self.current_style)

    def view_unsaved_changes(self):
        msg = "Unsaved Changes:\n"
        if not self.unsaved_changes:
            msg += "No unsaved changes"
        else:
            for section in self.unsaved_changes:
                msg += f"\n{section}:\n"
                for param in self.unsaved_changes[section]:
                    msg += f"{param}: {self.unsaved_changes[section][param]}\n"
        QMessageBox.information(self, "Unsaved Changes", msg)

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        # Check if there are unsaved changes
        if self.unsaved_changes:
            msg = "You have unsaved changes. Are you sure you want to exit?"
            reply = QMessageBox.question(
                self, "Unsaved Changes", msg, QMessageBox.Yes, QMessageBox.No
            )
            if reply == QMessageBox.No:
                a0.ignore()
                return


def run():
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    apply_stylesheet(app, theme="dark_blue.xml", css_file="gl-style-editor/custom.css")
    mainWin.show()
    sys.exit(app.exec_())
