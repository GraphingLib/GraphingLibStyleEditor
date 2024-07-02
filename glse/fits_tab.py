from PySide6.QtWidgets import QTabWidget, QVBoxLayout, QWidget, QFrame, QLabel
from PySide6.QtCore import Qt

from .widgets import Activator, ColorPickerWidget, Dropdown, Slider


def create_fits_tab(window):
    fits_layout = QVBoxLayout()
    fits_layout.setAlignment(Qt.AlignTop)

    confidence_curves_label = QLabel("Main Fit Curve:")
    confidence_curves_label.setStyleSheet("font-weight: bold;")
    fits_layout.addWidget(confidence_curves_label)

    confidence_curves_line = QFrame()
    confidence_curves_line.setFrameShape(QFrame.HLine)
    confidence_curves_line.setFrameShadow(QFrame.Sunken)
    fits_layout.addWidget(confidence_curves_line)

    # create color button with activator
    initial_color = (
        "#000000"
        if window.params["FitFromPolynomial"]["_color"] is None
        else window.params["FitFromPolynomial"]["_color"]
    )
    color = ColorPickerWidget(
        window,
        "Color",
        initial_color=initial_color,
        param_ids=[
            [
                "FitFromPolynomial",
                "FitFromExponential",
                "FitFromGaussian",
                "FitFromSine",
                "FitFromSquareRoot",
                "FitFromLog",
                "FitFromFunction",
                "FitFromFOTF",
            ],
            ["_color"],
        ],
        activated_on_init=window.params["FitFromPolynomial"]["_color"] is not None,
    )
    activator = Activator(
        window,
        color,
        param_ids=[
            [
                "FitFromPolynomial",
                "FitFromExponential",
                "FitFromGaussian",
                "FitFromSine",
                "FitFromSquareRoot",
                "FitFromLog",
                "FitFromFunction",
                "FitFromFOTF",
            ],
            "_color",
        ],
        check_label="Use color cycle",
        param_if_checked=None,
    )
    fits_layout.addWidget(activator)

    # create line_width slider
    line_width_slider = Slider(
        window,
        "Line Width:",
        0,
        20,
        1,
        [
            [
                "FitFromPolynomial",
                "FitFromExponential",
                "FitFromGaussian",
                "FitFromSine",
                "FitFromSquareRoot",
                "FitFromLog",
                "FitFromFunction",
                "FitFromFOTF",
            ],
            ["_line_width"],
        ],
        conversion_factor=2,
    )
    fits_layout.addWidget(line_width_slider)

    # create linestyle drop down menu
    line_style_dropdown = Dropdown(
        window,
        "Line Style:",
        ["Solid", "Dashed", "Dotted", "Dash-Dot"],
        ["-", "--", ":", "-."],
        [
            [
                "FitFromPolynomial",
                "FitFromExponential",
                "FitFromGaussian",
                "FitFromSine",
                "FitFromSquareRoot",
                "FitFromLog",
                "FitFromFunction",
                "FitFromFOTF",
            ],
            "_line_style",
        ],
    )
    fits_layout.addWidget(line_style_dropdown)

    confidence_curves_label = QLabel("Confidence Curves:")
    confidence_curves_label.setStyleSheet("font-weight: bold;")
    fits_layout.addWidget(confidence_curves_label)

    confidence_curves_line = QFrame()
    confidence_curves_line.setFrameShape(QFrame.HLine)
    confidence_curves_line.setFrameShadow(QFrame.Sunken)
    fits_layout.addWidget(confidence_curves_line)

    # create res_color button with activator
    initial_res_color = (
        "#000000"
        if window.params["FitFromPolynomial"]["_res_color"] is None
        else window.params["FitFromPolynomial"]["_res_color"]
    )
    res_color = ColorPickerWidget(
        window,
        "Confidence Curves Color",
        initial_color=initial_res_color,
        param_ids=[
            [
                "FitFromPolynomial",
                "FitFromExponential",
                "FitFromGaussian",
                "FitFromSine",
                "FitFromSquareRoot",
                "FitFromLog",
                "FitFromFunction",
                "FitFromFOTF",
            ],
            ["_res_color"],
        ],
        activated_on_init=window.params["FitFromPolynomial"]["_res_color"] is not None,
    )
    res_activator = Activator(
        window,
        res_color,
        param_ids=[
            [
                "FitFromPolynomial",
                "FitFromExponential",
                "FitFromGaussian",
                "FitFromSine",
                "FitFromSquareRoot",
                "FitFromLog",
                "FitFromFunction",
                "FitFromFOTF",
            ],
            "_res_color",
        ],
        check_label="Use color cycle",
        param_if_checked=None,
    )
    fits_layout.addWidget(res_activator)

    # create res_line_width slider
    res_line_width_slider = Slider(
        window,
        "Confidence Curves Width:",
        0,
        20,
        1,
        [
            [
                "FitFromPolynomial",
                "FitFromExponential",
                "FitFromGaussian",
                "FitFromSine",
                "FitFromSquareRoot",
                "FitFromLog",
                "FitFromFunction",
                "FitFromFOTF",
            ],
            ["_res_line_width"],
        ],
        conversion_factor=2,
    )
    fits_layout.addWidget(res_line_width_slider)

    # create res_linestyle drop down menu
    res_line_style_dropdown = Dropdown(
        window,
        "Confidence Curves Style:",
        ["Solid", "Dashed", "Dotted", "Dash-Dot"],
        ["-", "--", ":", "-."],
        [
            [
                "FitFromPolynomial",
                "FitFromExponential",
                "FitFromGaussian",
                "FitFromSine",
                "FitFromSquareRoot",
                "FitFromLog",
                "FitFromFunction",
                "FitFromFOTF",
            ],
            "_res_line_style",
        ],
    )
    fits_layout.addWidget(res_line_style_dropdown)

    return fits_layout
