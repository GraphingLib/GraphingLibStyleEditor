from PyQt5.QtWidgets import QVBoxLayout, QTabWidget, QWidget, QMainWindow


def create_plotting_2d_tab(window: QMainWindow):
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
    window.plotting2DTab.setLayout(layout)
