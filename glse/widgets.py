from typing import Optional

import matplotlib as mpl
from matplotlib.colors import is_color_like, to_hex
from cycler import cycler
from PySide6.QtCore import (
    QSortFilterProxyModel,
    QStringListModel,
    Qt,
    Signal,
    QPoint,
    QTimer,
)
from PySide6.QtGui import QColor, QFont, QIcon, QPainter, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QColorDialog,
    QComboBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QListView,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
    QSlider,
    QTableWidget,
    QTableWidgetItem,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


class ColorButton(QPushButton):
    colorChanged = Signal(str)

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
        dlg.setStyleSheet("background-color: #31363b;")
        if self._color:
            dlg.setCurrentColor(QColor(self._color))
            self.setStyleSheet(
                f"QPushButton {{ background-color: {self._color}; color: white; }}"
            )

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
        self.param_sections = param_ids[0]
        self.param_labels = param_ids[1]
        self.first_param_section = (
            self.param_sections[0]
            if isinstance(self.param_sections, list)
            else self.param_sections
        )
        self.first_param_label = (
            self.param_labels[0]
            if isinstance(self.param_labels, list)
            else self.param_labels
        )
        self.layout = QHBoxLayout(self)  # type: ignore

        self.label = QLabel(label)
        self.colorButton = ColorButton(color=initial_color)
        self.colorEdit = QLineEdit(initial_color)
        self.colorEdit.setFixedWidth(80)  # Half the length
        self.colorButton.colorChanged.connect(self.onColorChanged)
        self.colorEdit.textChanged.connect(self.onColorEditTextChanged)

        self.copyButton = QPushButton("Copy")
        self.pasteButton = QPushButton("Paste")
        self.copyButton.setFixedWidth(75)  # Shorter copy button
        self.pasteButton.setFixedWidth(75)  # Shorter paste button
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
        self.updating = False

    def onColorChanged(self, color):
        if not self.updating:
            self.updating = True
            if self.colorEdit.text() == "" or (
                color != self.colorEdit.text()
                and color != to_hex(self.colorEdit.text())
            ):
                self.colorEdit.setText(color)
                self.the_window.update_params(
                    self.param_sections, self.param_labels, color
                )
            self.updating = False

    def onColorEditTextChanged(self, text):
        if not self.updating:
            self.updating = True
            if QColor(text).isValid():
                self.colorButton.setColor(text)
                self.the_window.update_params(
                    self.param_sections, self.param_labels, text
                )
            elif is_color_like(text):
                # get the hex value of the color using matplotlib
                text = to_hex(text)
                self.colorButton.setColor(text)
                self.the_window.update_params(
                    self.param_sections, self.param_labels, text
                )
            self.updating = False

    def getValue(self):
        return self.colorButton._color


class Activator(QWidget):
    def __init__(
        self,
        window: QMainWindow,
        widget,
        param_ids=[],
        check_label="",
        param_if_checked: Optional[str] = "",
    ):
        super(Activator, self).__init__()
        self.the_window = window
        self.widget = widget
        self.param_sections = param_ids[0]
        self.param_labels = param_ids[1]
        self.first_param_section = (
            self.param_sections[0]
            if isinstance(self.param_sections, list)
            else self.param_sections
        )
        self.first_param_label = (
            self.param_labels[0]
            if isinstance(self.param_labels, list)
            else self.param_labels
        )
        self.layout = QHBoxLayout(self)  # type: ignore
        self.check_label = check_label
        self.param_if_checked = param_if_checked

        self.checkbox = QCheckBox(self.check_label)
        if (
            self.the_window.params[self.first_param_section][self.first_param_label]
            == param_if_checked
        ):

            is_checked = True
        else:
            is_checked = False
        self.checkbox.setChecked(is_checked)
        self.checkbox.stateChanged.connect(self.onStateChanged)
        self.widget.setEnabled(not is_checked)
        self.layout.addWidget(widget)
        self.layout.addWidget(self.checkbox)

    def onStateChanged(self, state):
        self.widget.setEnabled(True if state != 2 else False)
        if state == 2:
            new_param = self.param_if_checked
        else:
            new_param = self.widget.getValue()
        self.the_window.update_params(self.param_sections, self.param_labels, new_param)


class ActivatorDropdown(QWidget):
    """
    Same as Activator but with a dropdown instead of a checkbox
    Permits more than 2 options
    """

    def __init__(
        self,
        window: QMainWindow,
        widget,
        param_ids=[],
        active_label="",
        inactive_labels=[],
        params_if_inactive: list[str] = [],
    ):
        super(ActivatorDropdown, self).__init__()
        self.the_window = window
        self.widget = widget
        self.param_sections = param_ids[0]
        self.param_labels = param_ids[1]
        self.first_param_section = (
            self.param_sections[0]
            if isinstance(self.param_sections, list)
            else self.param_sections
        )
        self.first_param_label = (
            self.param_labels[0]
            if isinstance(self.param_labels, list)
            else self.param_labels
        )
        self.params_if_inactive = params_if_inactive
        self.active_label = active_label
        self.inactive_labels = inactive_labels

        self.layout = QHBoxLayout(self)  # type: ignore

        self.dropdown = QComboBox()
        self.dropdown.addItem(active_label)
        self.dropdown.addItems(inactive_labels)
        if (
            self.the_window.params[self.first_param_section][self.first_param_label]
            in params_if_inactive
        ):
            index = (
                params_if_inactive.index(
                    self.the_window.params[self.first_param_section][
                        self.first_param_label
                    ]
                )
                + 1
            )
        else:
            index = 0
        self.dropdown.setCurrentIndex(index)
        self.dropdown.currentIndexChanged.connect(self.onCurrentIndexChanged)
        self.widget.setEnabled(index == 0)
        self.layout.addWidget(widget)
        self.layout.addWidget(self.dropdown)

    def onCurrentIndexChanged(self, index):
        self.widget.setEnabled(index == 0)
        if index == 0:
            new_param = self.widget.getValue()
        else:
            current_text = self.dropdown.currentText()
            # get the index of the current text in the inactive labels
            text_index = self.dropdown.findText(current_text)
            # get the corresponding param from the params_if_inactive
            new_param = self.params_if_inactive[text_index - 1]
        self.the_window.update_params(self.param_sections, self.param_labels, new_param)


class Slider(QWidget):
    def __init__(
        self,
        window: QMainWindow,
        label,
        mini,
        maxi,
        tick_interval,
        param_ids=[],
        conversion_factor=2,
    ):
        super(Slider, self).__init__()
        self.the_window = window
        self.param_sections = param_ids[0]
        self.param_labels = param_ids[1]
        self.first_param_section = (
            self.param_sections[0]
            if isinstance(self.param_sections, list)
            else self.param_sections
        )
        self.first_param_label = (
            self.param_labels[0]
            if isinstance(self.param_labels, list)
            else self.param_labels
        )

        self.factor = conversion_factor

        self.label = QLabel(label)
        self.slider = QSlider(Qt.Horizontal)  # type: ignore
        self.slider.wheelEvent = lambda event: event.ignore()  # type: ignore
        self.slider.setMinimum(mini)
        self.slider.setMaximum(maxi)
        if isinstance(
            self.the_window.params[self.first_param_section][self.first_param_label],
            str,
        ):
            initial_value = 0
        else:
            initial_value = self.the_window.params[self.first_param_section][
                self.first_param_label
            ]
        self.slider.setValue(int(initial_value * self.factor))
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(tick_interval)
        self.slider.valueChanged.connect(self.onValueChanged)
        self.setEnabled(
            not isinstance(
                self.the_window.params[self.first_param_section][
                    self.first_param_label
                ],
                str,
            )
        )

        self.layout = QHBoxLayout(self)  # type: ignore
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.slider)

    def onValueChanged(self, value):
        new_value = value / self.factor
        # turn into int if it's a whole number
        if new_value == int(new_value):
            new_value = int(new_value)
        self.the_window.update_params(self.param_sections, self.param_labels, new_value)

    def getValue(self):
        return self.slider.value() / self.factor


class Dropdown(QWidget):
    def __init__(
        self,
        window: QMainWindow,
        label,
        items=[],
        param_values=[],
        param_ids=[],
    ):
        super(Dropdown, self).__init__()
        self.the_window = window
        self.param_sections = param_ids[0]
        self.param_labels = param_ids[1]
        self.first_param_section = (
            self.param_sections[0]
            if isinstance(self.param_sections, list)
            else self.param_sections
        )
        self.first_param_label = (
            self.param_labels[0]
            if isinstance(self.param_labels, list)
            else self.param_labels
        )
        self.param_values = param_values

        self.label = QLabel(label)
        self.dropdown = QComboBox()
        self.dropdown.addItems(items)
        if (
            isinstance(
                self.the_window.params[self.first_param_section][
                    self.first_param_label
                ],
                str,
            )
            and "same as"
            in self.the_window.params[self.first_param_section][self.first_param_label]
        ):
            initial_index = 0
        else:
            initial_index = self.param_values.index(
                self.the_window.params[self.first_param_section][self.first_param_label]
            )
        self.dropdown.setCurrentIndex(initial_index)
        self.dropdown.currentIndexChanged.connect(self.onCurrentIndexChanged)
        if (
            isinstance(
                self.the_window.params[self.first_param_section][
                    self.first_param_label
                ],
                str,
            )
            and "same as"
            in self.the_window.params[self.first_param_section][self.first_param_label]
        ):
            is_enabled = False
        else:
            is_enabled = True
        self.setEnabled(is_enabled)

        self.layout = QHBoxLayout(self)  # type: ignore
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.dropdown)

    def getValue(self):
        return self.dropdown.currentIndex()

    def onCurrentIndexChanged(self, index):
        self.the_window.update_params(
            self.param_sections, self.param_labels, self.param_values[index]
        )


class CheckBox(QWidget):
    def __init__(self, window: QMainWindow, label, param_ids=[]):
        super(CheckBox, self).__init__()
        self.checkbox = QCheckBox(label)
        self.the_window = window
        self.param_sections = param_ids[0]
        self.param_labels = param_ids[1]
        self.first_param_section = (
            self.param_sections[0]
            if isinstance(self.param_sections, list)
            else self.param_sections
        )
        self.first_param_label = (
            self.param_labels[0]
            if isinstance(self.param_labels, list)
            else self.param_labels
        )

        self.checkbox.setChecked(
            self.the_window.params[self.first_param_section][self.first_param_label]
        )
        self.checkbox.stateChanged.connect(self.onStateChanged)
        self.layout = QHBoxLayout(self)  # type: ignore
        self.layout.addWidget(self.checkbox)

    def onStateChanged(self, state):
        value = True if state == 2 else False
        self.the_window.update_params(self.param_sections, self.param_labels, value)


class IntegerBox(QWidget):
    def __init__(self, window: QMainWindow, label, param_ids=[]):
        super(IntegerBox, self).__init__()
        self.the_window = window
        self.param_sections = param_ids[0]
        self.param_labels = param_ids[1]
        self.first_param_section = (
            self.param_sections[0]
            if isinstance(self.param_sections, list)
            else self.param_sections
        )
        self.first_param_label = (
            self.param_labels[0]
            if isinstance(self.param_labels, list)
            else self.param_labels
        )

        self.label = QLabel(label)
        initial_value = self.the_window.params[self.first_param_section][
            self.first_param_label
        ]
        initial_value = 0 if isinstance(initial_value, str) else int(initial_value)
        self.spinbox = QSpinBox()
        self.spinbox.setValue(initial_value)
        self.spinbox.valueChanged.connect(self.onValueChanged)

        self.layout = QHBoxLayout(self)  # type: ignore
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.spinbox)

    def onValueChanged(self, value):
        self.the_window.update_params(self.param_sections, self.param_labels, value)

    def getValue(self):
        return self.spinbox.value()


class ListOptions(QWidget):
    def __init__(self, window: QMainWindow, label, options=[], param_ids=[]):
        super(ListOptions, self).__init__()
        self.the_window = window
        self.param_sections = param_ids[0]
        self.param_labels = param_ids[1]
        self.first_param_section = (
            self.param_sections[0]
            if isinstance(self.param_sections, list)
            else self.param_sections
        )
        self.first_param_label = (
            self.param_labels[0]
            if isinstance(self.param_labels, list)
            else self.param_labels
        )

        self.labelWidget = QLabel(label)
        self.filterLineEdit = QLineEdit()
        self.filterLineEdit.setPlaceholderText("Type to filter options...")
        self.listView = QListView()

        self.model = QStringListModel(options)

        self.proxyModel = QSortFilterProxyModel(self)
        self.proxyModel.setFilterCaseSensitivity(Qt.CaseInsensitive)  # type: ignore
        self.proxyModel.setSourceModel(self.model)
        self.listView.setModel(self.proxyModel)

        # Connect the QLineEdit's textChanged signal to update the filter
        self.filterLineEdit.textChanged.connect(self.proxyModel.setFilterFixedString)

        self.layout = QVBoxLayout(self)  # type: ignore
        self.layout.addWidget(self.labelWidget)
        self.layout.addWidget(self.filterLineEdit)
        self.layout.addWidget(self.listView)

        # Connect the listView selection change to handle selection
        self.listView.selectionModel().selectionChanged.connect(self.onSelectionChanged)

    def onSelectionChanged(self, selected, deselected):
        # Assuming the parameter needs the text of the selected option
        selectedIndexes = self.listView.selectedIndexes()
        if selectedIndexes:
            selectedText = self.model.data(selectedIndexes[0], Qt.DisplayRole)  # type: ignore
            self.the_window.update_params(
                self.param_sections, self.param_labels, selectedText
            )

    def getCurrentSelection(self):
        selectedIndexes = self.listView.selectedIndexes()
        if selectedIndexes:
            return self.model.data(selectedIndexes[0], Qt.DisplayRole)  # type: ignore
        return None


class IndicatorListWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.SingleSelection)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.list_widget)
        self.setLayout(self.layout)

        # Add items to the list with indicators

        # Sort items by their indicator color
        self.sort_items()

    def create_indicator_icon(self, is_gl, has_gl_twin=False):
        # Create a QPixmap object to draw on
        pixmap = QPixmap(40, 20)  # Increase width to accommodate two icons
        pixmap.fill(Qt.transparent)  # Ensure the background is transparent

        painter = QPainter(pixmap)
        colors = ["#3e82a0", "#edb73b", "#8aba4e"]
        # 3 color options. Teal for GL, Amber for non-GL, and Taupe for GL twin
        if is_gl and not has_gl_twin:  # GL
            color = QColor(colors[0])
            painter.setBrush(color)
            painter.drawEllipse(3, 3, 14, 14)  # Draw a filled circle
        elif not is_gl and not has_gl_twin:  # Custom
            color = QColor(colors[1])
            painter.setBrush(color)
            painter.drawRect(3, 3, 14, 14)  # Draw a filled square
        elif not is_gl and has_gl_twin:  # Custom with GL twin
            color = QColor(colors[2])
            painter.setBrush(color)
            # Draw a filled triangle
            painter.drawPolygon([QPoint(3, 17), QPoint(17, 17), QPoint(10, 3)])
        else:
            raise ValueError("Invalid combination of is_gl and has_gl_twin")

        painter.end()

        return QIcon(pixmap)

    def _add_item(self, text, is_gl, has_gl_twin=False):
        # Check that not both is_gl and has_gl_twin are True
        if is_gl and has_gl_twin:
            raise ValueError(
                "Both is_gl and has_gl_twin cannot be True. has_gl_twin is reserved for custom styles that share a name with a built-in style."
            )
        # Add item to the list widget with an indicator icon
        item = QListWidgetItem(text)
        item.setData(Qt.UserRole, (is_gl, has_gl_twin))
        icon = self.create_indicator_icon(is_gl, has_gl_twin)
        item.setIcon(icon)
        self.list_widget.addItem(item)

    def add_item(self, text, is_gl, has_gl_twin=False):
        # add and then sort items
        self._add_item(text, is_gl, has_gl_twin)
        self.sort_items()

    def add_items(self, gl_items, custom_items):
        # Add items to the list with indicators
        for item in custom_items:
            if item is None or item == "":
                continue
            if item in gl_items:
                self._add_item(item, is_gl=False, has_gl_twin=True)
            else:
                self._add_item(item, is_gl=False, has_gl_twin=False)
        for item in gl_items:
            if item not in custom_items:
                self._add_item(item, is_gl=True, has_gl_twin=False)

        # Sort items by their indicator color
        self.sort_items()

    def sort_items(self):
        # Sort items by their indicator state
        items = []
        for index in range(self.list_widget.count()):
            item = self.list_widget.item(index)
            items.append((item.data(Qt.UserRole), item.text()))

        # Sort items by their indicator state (reversed), and then by their text
        items.sort(key=lambda x: (x[0][0], x[1]))

        self.list_widget.clear()
        for state, text in items:
            self._add_item(text, *state)


class IconLabel(QWidget):
    def __init__(self, icon_type, text, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        label = QLabel(self)
        label.setText(text)
        label.setWordWrap(False)
        label.setFont(QFont("Arial", 12))
        label.setStyleSheet("color: #bfbfbf;")
        # set line height to 20px
        label.setFixedHeight(15)

        if icon_type == "GL":
            icon = self.create_indicator_icon(True, False)
        elif icon_type == "Custom":
            icon = self.create_indicator_icon(False, False)
        elif icon_type == "Twin":
            icon = self.create_indicator_icon(False, True)
        icon_label = QLabel(self)
        icon_label.setPixmap(icon.pixmap(10, 10))

        layout.addWidget(icon_label)
        layout.addWidget(label)
        layout.setAlignment(Qt.AlignLeft)
        self.setLayout(layout)

    def create_indicator_icon(self, is_gl, has_gl_twin=False):
        pixmap = QPixmap(20, 20)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        colors = ["#3e82a0", "#edb73b", "#8aba4e"]
        if is_gl and not has_gl_twin:
            color = QColor(colors[0])
            painter.setBrush(color)
            painter.drawEllipse(3, 3, 14, 14)
        elif not is_gl and not has_gl_twin:
            color = QColor(colors[1])
            painter.setBrush(color)
            painter.drawRect(3, 3, 14, 14)
        elif not is_gl and has_gl_twin:
            color = QColor(colors[2])
            painter.setBrush(color)
            painter.drawPolygon([QPoint(3, 17), QPoint(17, 17), QPoint(10, 3)])
        else:
            raise ValueError("Invalid combination of is_gl and has_gl_twin")

        painter.end()
        return QIcon(pixmap)


class TableWidget(QWidget):
    def __init__(self, window: QMainWindow, initial_dict=None):
        super().__init__()
        self.the_window = window
        self.layout = QVBoxLayout(self)

        self.table = QTableWidget(0, 3)
        self.table.setMaximumHeight(250)
        self.table.setHorizontalHeaderLabels(["Key", "Value", "Status"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.table)

        self.updating = False
        self.first_table_resize = False
        self.addButton = QPushButton("Add Row")
        self.deleteButton = QPushButton("Delete Row")
        self.addButton.clicked.connect(self.addRow)
        self.deleteButton.clicked.connect(self.deleteRow)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.addButton)
        buttonLayout.addWidget(self.deleteButton)
        self.layout.addLayout(buttonLayout)

        self.handled_elsewhere = [
            "figure.facecolor",
            "axes.facecolor",
            "axes.edgecolor",
            "axes.labelcolor",
            "axes.linewidth",
            "axes.prop_cycle",
            "xtick.color",
            "ytick.color",
            "xtick.direction",
            "ytick.direction",
            "legend.facecolor",
            "legend.edgecolor",
            "font.family",
            "font.size",
            "lines.solid_capstyle",
            "lines.dash_joinstyle",
            "lines.dash_capstyle",
            "grid.linestyle",
            "grid.linewidth",
            "grid.color",
            "grid.alpha",
            "axes.grid",
        ]

        self.initial_dict = initial_dict if initial_dict else {}
        self.initial_dict = {
            k: str(v)
            for k, v in self.initial_dict.items()
            if k not in self.handled_elsewhere
        }

        self.populateTable()

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.updateTableHeight)
        self.timer.start(100)

        valid_data = self.getTableData()
        self.the_window.update_rc_params_from_table(valid_data, init=True)
        self.table.itemChanged.connect(self.onTableItemChanged)

        self.addLegend()

    def addLegend(self):
        legend_layout = QHBoxLayout()
        valid_icon = self.create_indicator_icon("Valid")
        invalid_icon = self.create_indicator_icon("Invalid Value")
        handled_icon = self.create_indicator_icon("Handled Elsewhere")

        valid_label = QLabel()
        valid_label.setPixmap(valid_icon.pixmap(20, 20))
        invalid_label = QLabel()
        invalid_label.setPixmap(invalid_icon.pixmap(20, 20))
        handled_label = QLabel()
        handled_label.setPixmap(handled_icon.pixmap(20, 20))

        legend_layout.addWidget(QLabel("Valid key/value:"))
        legend_layout.addWidget(valid_label)
        legend_layout.addWidget(QLabel("Invalid key/value:"))
        legend_layout.addWidget(invalid_label)
        legend_layout.addWidget(QLabel("Ignored (set elsewhere in GLSE):"))
        legend_layout.addWidget(handled_label)

        self.layout.addLayout(legend_layout)

    def populateTable(self):
        for key, value in self.initial_dict.items():
            self.addRow(key, value, init=True)
        self.validateTable()

    def addRow(self, key="", value="", init=False):
        if not self.updating:
            self.updating = True
            rowPosition = self.table.rowCount()
            self.table.insertRow(rowPosition)
            keyItem = QTableWidgetItem(key)
            valueItem = QTableWidgetItem(value)
            statusItem = QTableWidgetItem("")
            self.table.setItem(rowPosition, 0, keyItem)
            self.table.setItem(rowPosition, 1, valueItem)
            self.table.setItem(rowPosition, 2, statusItem)
            keyItem.setFlags(keyItem.flags() | Qt.ItemIsEditable)
            valueItem.setFlags(valueItem.flags() | Qt.ItemIsEditable)
            statusItem.setFlags(statusItem.flags() & ~Qt.ItemIsEditable)
            statusItem.setTextAlignment(Qt.AlignCenter)
            valid_data = self.getTableData()
            if not init:
                self.the_window.update_rc_params_from_table(valid_data)
            self.updateTableHeight()
            self.updating = False

    def deleteRow(self):
        if not self.updating:
            self.updating = True
            rowPosition = self.table.currentRow()
            if bool(self.table.selectedItems()):
                self.table.removeRow(rowPosition)
            else:
                self.table.removeRow(self.table.rowCount() - 1)
            self.updateTableHeight()
            valid_data = self.getTableData()
            self.the_window.update_rc_params_from_table(valid_data)
            self.updating = False

    def getTableData(self):
        data_dict = {}
        for row in range(self.table.rowCount()):
            keyItem = self.table.item(row, 0)
            valueItem = self.table.item(row, 1)
            statusItem = self.table.item(row, 2)
            if keyItem and valueItem and statusItem:
                status = statusItem.data(Qt.UserRole)
                if status == "Valid":
                    data_dict[keyItem.text()] = valueItem.text()
        return data_dict

    def updateTableHeight(self):
        row_count = self.table.rowCount()
        if row_count == 0:
            self.table.setFixedHeight(50)  # Minimum height for empty table
        else:
            row_height = self.table.rowHeight(0)
            header_height = self.table.horizontalHeader().height()
            total_height = row_count * row_height + header_height
            self.table.setFixedHeight(min(total_height, 250))

    def onTableItemChanged(self, item):
        if not self.updating:
            self.updating = True
            self.validateRow(item.row())
            valid_data = self.getTableData()
            self.the_window.update_rc_params_from_table(valid_data)
            self.updating = False

    def validateRow(self, row) -> bool:
        key = self.table.item(row, 0).text()
        value = self.table.item(row, 1).text()
        statusItem = self.table.item(row, 2)

        is_valid = False
        try:
            # get original value
            original_value = mpl.rcParams[key]
            # try to set the value to see if it's valid
            mpl.rcParams[key] = value
            # reset the value to the original value
            mpl.rcParams[key] = original_value
        except (ValueError, KeyError, TypeError):
            icon = self.create_indicator_icon("Invalid Value")
            statusItem.setIcon(icon)
            statusItem.setData(Qt.UserRole, "Invalid Value")
            statusItem.setToolTip("Invalid key/value pair, will be ignored")
            is_valid = False
        else:
            if key in self.handled_elsewhere:
                icon = self.create_indicator_icon("Handled Elsewhere")
                statusItem.setIcon(icon)
                statusItem.setData(Qt.UserRole, "Handled Elsewhere")
                statusItem.setToolTip(
                    "This key is set elsewhere in GLSE and will be ignored"
                )
                is_valid = False
            else:
                icon = self.create_indicator_icon("Valid")
                statusItem.setIcon(icon)
                statusItem.setData(Qt.UserRole, "Valid")
                statusItem.setToolTip("Valid key/value pair")
                is_valid = True
        return is_valid

    def validateTable(self):
        for row in range(self.table.rowCount()):
            self.validateRow(row)

    def create_indicator_icon(self, status):
        pixmap = QPixmap(20, 20)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        if status == "Valid":
            color = QColor("#8aba4e")  # Green
            painter.setBrush(color)
            painter.drawEllipse(3, 3, 14, 14)
        elif status == "Invalid Value":
            color = QColor("#ed3e3e")  # Red
            painter.setBrush(color)
            painter.drawRect(3, 3, 14, 14)
        elif status == "Handled Elsewhere":
            color = QColor("#edb73b")  # Yellow
            painter.setBrush(color)
            painter.drawPolygon([QPoint(3, 17), QPoint(17, 17), QPoint(10, 3)])
        else:
            color = QColor(Qt.transparent)  # No icon
        painter.end()

        return QIcon(pixmap)


class ColorCycleWidget(QWidget):
    colorsUpdated = Signal(list)

    def __init__(self, window, label="Color Cycle:", initial_colors=None):
        super().__init__()
        self.the_window = window
        self.layout = QVBoxLayout(self)
        self.label = QLabel(label)
        self.layout.addWidget(self.label)
        self.colors_layout = QVBoxLayout()
        self.layout.addLayout(self.colors_layout)
        self.add_button = QPushButton("Add Color")
        self.add_button.clicked.connect(self.add_color)
        self.layout.addWidget(self.add_button)

        self.color_widgets = []

        if initial_colors is None:
            initial_colors = ["#ff0000", "#00ff00", "#0000ff"]
        for color in initial_colors:
            self.add_color_widget(color)

        self.colorsUpdated.connect(self.update_window_params)

    def add_color_widget(self, color="#000000"):
        color_widget = ColorPickerForCycleWidget(
            self, initial_color=color, param_ids=[[], []]
        )
        color_widget.colorChanged.connect(self.onColorChanged)
        remove_button = QPushButton("Remove")
        remove_button.clicked.connect(lambda: self.remove_color_widget(color_widget))
        color_widget.layout.addWidget(remove_button)
        self.colors_layout.addWidget(color_widget)
        self.color_widgets.append(color_widget)
        self.onColorChanged()

    def remove_color_widget(self, color_widget):
        self.colors_layout.removeWidget(color_widget)
        color_widget.setParent(None)
        self.color_widgets.remove(color_widget)
        self.onColorChanged()

    def add_color(self):
        self.add_color_widget()

    def get_colors(self):
        return [widget.getValue() for widget in self.color_widgets]

    def onColorChanged(self):
        colors = self.get_colors()
        self.colorsUpdated.emit(colors)

    def update_window_params(self, colors):
        cycle = cycler(color=colors)
        self.the_window.update_params(["rc_params"], ["axes.prop_cycle"], cycle)


class ColorPickerForCycleWidget(QWidget):
    colorChanged = Signal(str)

    def __init__(
        self,
        window: QWidget,
        label="Pick a colour:",
        initial_color="#ff0000",
        param_ids=[],
        activated_on_init=True,
    ):
        super().__init__()
        self.the_window = window
        self.param_sections = param_ids[0]
        self.param_labels = param_ids[1]
        self.first_param_section = (
            self.param_sections[0]
            if isinstance(self.param_sections, list) and self.param_sections
            else None
        )
        self.first_param_label = (
            self.param_labels[0]
            if isinstance(self.param_labels, list) and self.param_labels
            else None
        )
        self.layout = QHBoxLayout(self)  # type: ignore

        self.label = QLabel(label)
        self.colorButton = ColorButton(color=initial_color)
        self.colorEdit = QLineEdit(initial_color)
        self.colorEdit.setFixedWidth(80)  # Half the length
        self.colorButton.colorChanged.connect(self.onColorChanged)
        self.colorEdit.textChanged.connect(self.onColorEditTextChanged)

        self.copyButton = QPushButton("Copy")
        self.pasteButton = QPushButton("Paste")
        self.copyButton.setFixedWidth(75)  # Shorter copy button
        self.pasteButton.setFixedWidth(75)  # Shorter paste button
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
        self.updating = False

    def onColorChanged(self, color):
        if not self.updating:
            self.updating = True
            if self.colorEdit.text() == "" or (
                color != self.colorEdit.text()
                and color != to_hex(self.colorEdit.text())
            ):
                self.colorEdit.setText(color)
                self.colorChanged.emit(color)  # Emit signal with color as parameter
            self.updating = False

    def onColorEditTextChanged(self, text):
        if not self.updating:
            self.updating = True
            if QColor(text).isValid():
                self.colorButton.setColor(text)
                self.colorChanged.emit(text)  # Emit signal with text as parameter
            elif is_color_like(text):
                # get the hex value of the color using matplotlib
                text = to_hex(text)
                self.colorButton.setColor(text)
                self.colorChanged.emit(text)  # Emit signal with text as parameter
            self.updating = False

    def getValue(self):
        return self.colorButton.color()
