from typing import Optional

from matplotlib.colors import is_color_like, to_hex
from PySide6.QtCore import QSortFilterProxyModel, QStringListModel, Qt, Signal
from PySide6.QtGui import QColor, QFont, QIcon, QPainter, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QColorDialog,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListView,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
    QSlider,
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
        self.param_section = param_ids[0]
        self.param_labels = param_ids[1]
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
                    self.param_section, self.param_labels, color
                )
            self.updating = False

    def onColorEditTextChanged(self, text):
        if not self.updating:
            self.updating = True
            if QColor(text).isValid():
                self.colorButton.setColor(text)
                self.the_window.update_params(
                    self.param_section, self.param_labels, text
                )
            elif is_color_like(text):
                # get the hex value of the color using matplotlib
                text = to_hex(text)
                self.colorButton.setColor(text)
                self.the_window.update_params(
                    self.param_section, self.param_labels, text
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
        self.param_section = param_ids[0]
        self.param_label = param_ids[1]
        self.layout = QHBoxLayout(self)  # type: ignore
        self.check_label = check_label
        self.param_if_checked = param_if_checked

        self.checkbox = QCheckBox(self.check_label)
        if (
            self.the_window.params[self.param_section][self.param_label]
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
        self.the_window.update_params(self.param_section, self.param_label, new_param)


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
        self.param_section = param_ids[0]
        self.param_label = param_ids[1]
        self.factor = conversion_factor

        self.label = QLabel(label)
        self.slider = QSlider(Qt.Horizontal)  # type: ignore
        self.slider.wheelEvent = lambda event: event.ignore()  # type: ignore
        self.slider.setMinimum(mini)
        self.slider.setMaximum(maxi)
        if isinstance(
            self.the_window.params[self.param_section][self.param_label], str
        ):
            initial_value = 0
        else:
            initial_value = self.the_window.params[self.param_section][self.param_label]
        self.slider.setValue(int(initial_value * self.factor))
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(tick_interval)
        self.slider.valueChanged.connect(self.onValueChanged)
        self.setEnabled(
            not isinstance(
                self.the_window.params[self.param_section][self.param_label], str
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
        self.the_window.update_params(self.param_section, self.param_label, new_value)

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
        self.param_section = param_ids[0]
        self.param_label = param_ids[1]
        self.param_values = param_values

        self.label = QLabel(label)
        self.dropdown = QComboBox()
        self.dropdown.addItems(items)
        if (
            isinstance(
                self.the_window.params[self.param_section][self.param_label], str
            )
            and "same as"
            in self.the_window.params[self.param_section][self.param_label]
        ):
            initial_index = 0
        else:
            initial_index = self.param_values.index(
                self.the_window.params[self.param_section][self.param_label]
            )
        self.dropdown.setCurrentIndex(initial_index)
        self.dropdown.currentIndexChanged.connect(self.onCurrentIndexChanged)
        if (
            isinstance(
                self.the_window.params[self.param_section][self.param_label], str
            )
            and "same as"
            in self.the_window.params[self.param_section][self.param_label]
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
            self.param_section, self.param_label, self.param_values[index]
        )


class CheckBox(QWidget):
    def __init__(self, window: QMainWindow, label, param_ids=[]):
        super(CheckBox, self).__init__()
        self.checkbox = QCheckBox(label)
        self.the_window = window
        self.param_section = param_ids[0]
        self.param_label = param_ids[1]

        self.checkbox.setChecked(
            self.the_window.params[self.param_section][self.param_label]
        )
        self.checkbox.stateChanged.connect(self.onStateChanged)
        self.layout = QHBoxLayout(self)  # type: ignore
        self.layout.addWidget(self.checkbox)

    def onStateChanged(self, state):
        value = True if state == 2 else False
        self.the_window.update_params(self.param_section, self.param_label, value)


class IntegerBox(QWidget):
    def __init__(self, window: QMainWindow, label, param_ids=[]):
        super(IntegerBox, self).__init__()
        self.the_window = window
        self.param_section = param_ids[0]
        self.param_label = param_ids[1]

        self.label = QLabel(label)
        initial_value = self.the_window.params[self.param_section][self.param_label]
        initial_value = 0 if isinstance(initial_value, str) else int(initial_value)
        self.spinbox = QSpinBox()
        self.spinbox.setValue(initial_value)
        self.spinbox.valueChanged.connect(self.onValueChanged)

        self.layout = QHBoxLayout(self)  # type: ignore
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.spinbox)

    def onValueChanged(self, value):
        self.the_window.update_params(self.param_section, self.param_label, value)

    def getValue(self):
        return self.spinbox.value()


class ListOptions(QWidget):
    def __init__(self, window: QMainWindow, label, options=[], param_ids=[]):
        super(ListOptions, self).__init__()
        self.the_window = window
        self.param_section = param_ids[0]
        self.param_label = param_ids[1]

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
                self.param_section, self.param_label, selectedText
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
        color = QColor("blue") if is_gl else QColor("green")
        painter.setBrush(color)
        painter.drawEllipse(3, 3, 14, 14)  # Draw a filled circle

        # Draw the letter '2' if has_gl_twin is True
        if has_gl_twin:
            painter.setFont(QFont("Arial", 20))
            painter.setPen(QColor("grey"))
            painter.drawText(25, 17, "2")

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
