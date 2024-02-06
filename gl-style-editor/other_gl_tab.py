from PyQt5.QtWidgets import QVBoxLayout, QTabWidget, QWidget


def create_other_gl_tab(window):
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
    window.otherGLTab.setLayout(layout)
