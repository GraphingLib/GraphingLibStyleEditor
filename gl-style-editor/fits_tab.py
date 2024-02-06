from PyQt5.QtWidgets import QVBoxLayout, QTabWidget, QWidget


def create_fits_tab(window):
    layout = QVBoxLayout()
    tabWidget = QTabWidget()

    fitFromPolynomialTab = QWidget()
    tabWidget.addTab(fitFromPolynomialTab, "Polynomial")
    fitFromSineTab = QWidget()
    tabWidget.addTab(fitFromSineTab, "Sine")
    fitFromExponentialTab = QWidget()
    tabWidget.addTab(fitFromExponentialTab, "Exponential")
    fitFromGaussianTab = QWidget()
    tabWidget.addTab(fitFromGaussianTab, "Gaussian")
    fitFromLogTab = QWidget()
    tabWidget.addTab(fitFromLogTab, "Log")
    fitFromSquareRootTab = QWidget()
    tabWidget.addTab(fitFromSquareRootTab, "Square Root")
    fitFromFunctionTab = QWidget()
    tabWidget.addTab(fitFromFunctionTab, "Function")

    layout.addWidget(tabWidget)
    window.fitsTab.setLayout(layout)
