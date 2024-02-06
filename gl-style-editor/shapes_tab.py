from PyQt5.QtWidgets import QVBoxLayout, QTabWidget, QWidget


def create_shapes_tab(window):
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
    window.shapesTab.setLayout(layout)
