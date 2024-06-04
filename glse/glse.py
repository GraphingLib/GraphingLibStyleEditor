import os
import sys

import graphinglib as gl
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.pyplot import close
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent, QKeySequence
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QDialog,
    QFileDialog,
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
from .widgets import IndicatorListWidget


class GLCanvas(FigureCanvas):
    def __init__(self, fig):
        self.fig = fig
        super(GLCanvas, self).__init__(self.fig)


class FigureManager(QWidget):
    def __init__(self, params: dict, which_figure: str = "curve"):
        super().__init__()
        self.layout = QVBoxLayout()
        self.button = QPushButton("Load Figure from file")
        self.button.clicked.connect(self.load_python_file)
        # Create list of example figures to choose from
        self.horiz1_layout = QHBoxLayout()
        self.exampleFigures = QListWidget()
        self.example_figs_dict = {
            os.path.splitext(f)[0]: f
            for f in os.listdir(os.path.join(os.path.dirname(__file__), "figures"))
        }
        self.exampleFigures.addItems(self.example_figs_dict.keys())
        self.exampleFigures.setSelectionMode(QListWidget.SingleSelection)
        self.exampleFigures.itemSelectionChanged.connect(self.choose_builtin_figure)
        self.exampleFigures.setFixedWidth(200)
        self.exampleFigures.setFixedHeight(100)
        # Add auto switch checkbox
        self.autoSwitchCheckbox = QCheckBox("Auto Switch")
        self.autoSwitchCheckbox.setChecked(True)
        self.auto_switch_is_on = True
        self.autoSwitchCheckbox.stateChanged.connect(self.toggle_auto_switch)
        self.horiz1_layout.addWidget(self.autoSwitchCheckbox)
        self.horiz1_layout.addWidget(self.exampleFigures)
        self.layout.addLayout(self.horiz1_layout)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)
        self.which_figure = which_figure
        self.params = params
        self.chosen = None
        self.canvas = None
        # Check if figure is a path or just name
        if not self.which_figure.endswith(".py"):
            figures = os.listdir(os.path.join(os.path.dirname(__file__), "figures"))
            if self.which_figure + ".py" in figures:
                self.which_figure = os.path.join(
                    os.path.dirname(__file__), "figures", self.which_figure + ".py"
                )
            else:
                raise FileNotFoundError(
                    f"Figure {self.which_figure} not found in figures directory"
                )
        self.execute_python_file(self.which_figure)

    def load_python_file(self):
        filepath, _ = QFileDialog.getOpenFileName(
            self, "Open Python file", "", "Python Files (*.py)"
        )
        if filepath:
            self.chosen = None
            self.which_figure = filepath
            # turn off auto switch
            self.autoSwitchCheckbox.setChecked(False)
            self.auto_switch_is_on = False
            self.execute_python_file(filepath)

    def choose_builtin_figure(self):
        self.chosen = None
        chosen_fig = self.exampleFigures.currentItem().text()
        self.which_figure = os.path.join(
            os.path.dirname(__file__), "figures", self.example_figs_dict[chosen_fig]
        )

        self.execute_python_file(
            os.path.join(
                os.path.dirname(__file__), "figures", self.example_figs_dict[chosen_fig]
            )
        )

    def execute_python_file(self, filepath):
        # Clear the canvas widget
        for i in reversed(range(self.layout.count())):
            widgetToRemove = self.layout.itemAt(i).widget()
            if widgetToRemove is self.canvas and self.canvas is not None:
                self.layout.removeWidget(widgetToRemove)
                widgetToRemove.setParent(None)
        close("all")

        original_show = gl.Figure.show
        original_save = gl.Figure.save
        original_multi_show = gl.MultiFigure.show
        original_multi_save = gl.MultiFigure.save
        gl.Figure.show = self.dummy_show
        gl.Figure.save = self.dummy_save
        gl.MultiFigure.show = self.dummy_show
        gl.MultiFigure.save = self.dummy_save

        # Execute the script
        namespace = {"gl": gl, "__builtins__": __builtins__}
        with open(filepath) as file:
            code = compile(file.read(), filepath, "exec")
            exec(code, namespace, namespace)

        gl.Figure.show = original_show
        gl.Figure.save = original_save
        gl.MultiFigure.show = original_multi_show
        gl.MultiFigure.save = original_multi_save
        # Check for figures in the namespace and display them
        figures = {}
        for name, var in namespace.items():
            if isinstance(var, gl.Figure) or isinstance(var, gl.MultiFigure):
                figures[name] = var

        # Popup to ask user which figure to display
        if self.chosen is None:
            if len(figures) > 1:
                self.chosen = self.choose_figure_from_file(figures.keys())
            else:
                self.chosen = list(figures.keys())[0]

        if self.chosen is not None:
            fig = figures[self.chosen]
            if isinstance(fig, gl.MultiFigure):
                fig._prepare_multi_figure()
            elif isinstance(fig, gl.Figure):
                fig.figure_style = "plain"
                fig._prepare_figure(default_params=self.params)
            self.display_figure(fig._figure)

    def display_figure(self, fig):
        self.canvas = GLCanvas(fig)
        # add widget to layout in position 1 (after the button)
        self.layout.insertWidget(0, self.canvas)
        # self.layout.addWidget(self.canvas)
        # canvas.draw()

    def choose_figure_from_file(self, figures):
        chosen, ok = QInputDialog.getItem(
            self, "Choose Figure", "Select a figure to display", figures, 0, False
        )
        if ok:
            return chosen
        return None

    def update(self, params):
        self.params = params
        self.execute_python_file(self.which_figure)

    def toggle_auto_switch(self):
        self.auto_switch_is_on = self.autoSwitchCheckbox.isChecked()

    def tab_changed_to(self, tab_name):
        tab_name = tab_name.lower()
        if tab_name in self.example_figs_dict.keys():
            self.exampleFigures.setCurrentRow(
                list(self.example_figs_dict.keys()).index(tab_name)
            )

    def dummy_show(*args, **kwargs):
        pass

    def dummy_save(*args, **kwargs):
        pass


class StyleManager(QDialog):
    def __init__(self, parent=None):
        super(StyleManager, self).__init__(parent)
        self.setWindowTitle("Manage Styles")
        self.setGeometry(100, 100, 460, 200)

        # Add label for default style
        self.default_style_label = QLabel(self)
        self.default_style_label.setText(f"Default Style: {gl.get_default_style()}")

        # Add list of styles to select from
        self.styles = gl.get_styles(
            gl=True, customs=True, matplotlib=False, as_dict=True
        )
        self.styleList = IndicatorListWidget()
        self.styleList.add_items(
            gl_items=self.styles["gl"], custom_items=self.styles["customs"]
        )
        # self.styleList.setSelectionMode(QListWidget.SingleSelection)
        self.current_selection = None
        self.styleList.list_widget.itemSelectionChanged.connect(self.update_selection)

        # Explanation label
        self.explanationLabel = QLabel(self)
        self.explanationLabel.setText(
            "Green: Custom style\nBlue: Built-in style\n2: This is a custom style that overrides a built-in style of the same name."
        )
        self.explanationLabel.setWordWrap(True)
        self.explanationLabel.setStyleSheet("color: #bfbfbf")

        # Add buttons to delete, rename styles, and set a style as the default
        self.renameButton = QPushButton("Rename", self)
        self.renameButton.clicked.connect(self.rename_style)
        self.deleteButton = QPushButton("Delete", self)
        self.deleteButton.clicked.connect(self.delete_style)
        self.duplicateButton = QPushButton("Duplicate", self)
        self.duplicateButton.clicked.connect(self.duplicate_style)
        self.defaultButton = QPushButton("Set as default", self)
        self.defaultButton.clicked.connect(self.set_default_style)

        # Add layouts
        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(self.renameButton)
        buttonLayout.addWidget(self.deleteButton)
        buttonLayout.addWidget(self.duplicateButton)
        buttonLayout.addWidget(self.defaultButton)
        main_h_layout = QHBoxLayout()
        main_h_layout.addWidget(self.styleList)
        main_h_layout.addLayout(buttonLayout)
        v_layout_1 = QVBoxLayout()
        v_layout_1.addWidget(self.default_style_label)
        v_layout_1.addLayout(main_h_layout)
        v_layout_1.addWidget(self.explanationLabel)
        self.setLayout(v_layout_1)

        self.shortcut_close = QShortcut(QKeySequence("Ctrl+W"), self)
        self.shortcut_close.activated.connect(self.close)

    def update_selection(self):
        self.current_selection = self.styleList.list_widget.currentItem().text()

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
                if gl.get_default_style() == self.current_selection:
                    gl.set_default_style("plain")
                    self.default_style_label.setText(
                        f"Default Style: {gl.get_default_style()}"
                    )
                gl.file_manager.FileDeleter(self.current_selection).delete()
                self.styleList.list_widget.clear()
                self.styles = gl.get_styles(
                    gl=True, customs=True, matplotlib=False, as_dict=True
                )
                self.styleList.add_items(
                    gl_items=self.styles["gl"], custom_items=self.styles["customs"]
                )
                self.current_selection = None

    def rename_style(self):
        if not self.current_selection:
            return
        # check if the current selection is in custom styles
        if self.current_selection not in gl.get_styles(
            gl=False, customs=True, matplotlib=False
        ):
            msg = "You can only rename custom styles. If you want to rename a built-in style, you must duplicate it first."
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
            elif ok and name in gl.get_styles(gl=False, customs=True, matplotlib=False):
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
            self.styleList.list_widget.clear()
            self.styles = gl.get_styles(
                gl=True, customs=True, matplotlib=False, as_dict=True
            )
            self.styleList.add_items(
                gl_items=self.styles["gl"], custom_items=self.styles["customs"]
            )
            self.current_selection = None
            gl.set_default_style(name)
            self.default_style_label.setText(f"Default Style: {gl.get_default_style()}")

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
            elif ok and name in gl.get_styles(gl=False, customs=True, matplotlib=False):
                msg = "This style already exists. Please enter a new name."
                QMessageBox.information(self, "Invalid Name", msg)
            else:
                bad_name = False

        if ok:
            params = gl.file_manager.FileLoader(self.current_selection).load()
            gl.file_manager.FileSaver(name, params).save()
            self.styleList.list_widget.clear()
            self.styles = gl.get_styles(
                gl=True, customs=True, matplotlib=False, as_dict=True
            )
            self.styleList.add_items(
                gl_items=self.styles["gl"], custom_items=self.styles["customs"]
            )
            self.current_selection = None

    def set_default_style(self):
        if not self.current_selection:
            return

        gl.set_default_style(self.current_selection)

        self.default_style_label.setText(f"Default Style: {gl.get_default_style()}")


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
        self.current_style = gl.get_default_style()
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
        self.canvas = FigureManager(self.params, which_figure="curve")
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

        # Add tab changed event to update the canvas
        self.tabWidget.currentChanged.connect(self.tab_changed)

        # 1D Plotting tab with nested tabs
        self.plotting1DTab = QWidget()
        self.tabWidget.addTab(self.plotting1DTab, "1D Plotting")
        self.tab_widget_1d = create_plotting_1d_tab(self)
        self.tab_widget_1d.currentChanged.connect(self.sub_tab_changed)

        # 2D Plotting tab with nested tabs
        self.plotting2DTab = QWidget()
        self.tabWidget.addTab(self.plotting2DTab, "2D Plotting")
        self.tab_widget_2d = create_plotting_2d_tab(self)
        self.tab_widget_2d.currentChanged.connect(self.sub_tab_changed)

        # Fits tab with nested tabs
        self.fitsTab = QWidget()
        self.tabWidget.addTab(self.fitsTab, "Fits")
        self.tab_widget_fits = create_fits_tab(self)
        self.tab_widget_fits.currentChanged.connect(self.sub_tab_changed)

        # Shapes tab with nested tabs
        self.shapesTab = QWidget()
        self.tabWidget.addTab(self.shapesTab, "Shapes")
        self.tab_widget_shapes = create_shapes_tab(self)
        self.tab_widget_shapes.currentChanged.connect(self.sub_tab_changed)

        # Other GL Objects tab with nested tabs
        self.otherGLTab = QWidget()
        self.tabWidget.addTab(self.otherGLTab, "Other GL Objects")
        self.tab_widget_other_gl = create_other_gl_tab(self)
        self.tab_widget_other_gl.currentChanged.connect(self.sub_tab_changed)

    def updateFigure(self):
        # Update the figure after changing parameters
        self.canvas.update(self.params)

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
            auto_switch_original = self.canvas.auto_switch_is_on
            self.canvas.auto_switch_is_on = False
            for i in range(self.tabWidget.count()):
                self.tabWidget.removeTab(0)
            self.create_tabs()
            # set the current tab
            self.tabWidget.setCurrentIndex(current_tab)
            if current_sub_tab is not None:
                self.tabWidget.currentWidget().layout().itemAt(
                    0
                ).widget().setCurrentIndex(current_sub_tab)
            self.canvas.auto_switch_is_on = auto_switch_original

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
        if self.current_style not in gl.get_styles(gl=True, customs=True):
            self.current_style = gl.get_default_style()
        self.params = gl.file_manager.FileLoader(self.current_style).load()
        self.updateFigure()
        # remove all tabs and recreate them to update the params
        auto_switch_original = self.canvas.auto_switch_is_on
        self.canvas.auto_switch_is_on = False
        for i in range(self.tabWidget.count()):
            self.tabWidget.removeTab(0)
        self.create_tabs()
        self.canvas.auto_switch_is_on = auto_switch_original
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

    def tab_changed(self, index):
        if not self.canvas.auto_switch_is_on:
            return
        # get name of current tab
        current_tab = self.tabWidget.tabText(self.tabWidget.currentIndex())
        # get current sub tab if it exists
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
        if current_tab is not None:
            try:
                # Get name of current sub tab
                current_sub_tab = (
                    self.tabWidget.currentWidget()
                    .layout()
                    .itemAt(0)
                    .widget()
                    .tabText(
                        self.tabWidget.currentWidget()
                        .layout()
                        .itemAt(0)
                        .widget()
                        .currentIndex()
                    )
                )
            except:
                current_sub_tab = None
            if current_sub_tab is not None:
                self.canvas.tab_changed_to(current_sub_tab)

    def sub_tab_changed(self, index):
        if not self.canvas.auto_switch_is_on:
            return
        # get name of current tab
        current_tab = self.tabWidget.tabText(self.tabWidget.currentIndex())
        # get current sub tab if it exists
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
        if current_tab is not None:
            # Get name of current sub tab
            try:
                current_sub_tab = (
                    self.tabWidget.currentWidget()
                    .layout()
                    .itemAt(0)
                    .widget()
                    .tabText(
                        self.tabWidget.currentWidget()
                        .layout()
                        .itemAt(0)
                        .widget()
                        .currentIndex()
                    )
                )
            except:
                current_sub_tab = None
            self.canvas.tab_changed_to(current_sub_tab)

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
