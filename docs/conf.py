# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import time
from glse import __version__

project = "GraphingLib Style Editor"
copyright = f"{time.strftime('%Y')}, Gustave Coulombe, Yannick Lapointe"
author = "Gustave Coulombe and Yannick Lapointe"
release = __version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx_favicon",
    "sphinx_design",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
html_context = {"default_mode": "dark"}
html_show_sourcelink = False
html_css_files = ["graphinglib.css"]
html_theme_options = {
    "logo": {
        "text": "Style Editor",
        "image_dark": "_static/GraphingLib-SE-Logo.svg",
        "image_light": "_static/GraphingLib-SE-Logo.svg",
    },
    "github_url": "https://github.com/GraphingLib/GraphingLibStyleEditor",
    "show_prev_next": False,
    "show_toc_level": 2,
    "header_links_before_dropdown": 10,
    "pygment_light_style": "tango",
    "pygment_dark_style": "github-dark",
}
html_static_path = ["_static"]
html_sidebars = {"handbook": [], "compatibility": []}
favicons = ["GraphingLib-favicon_250x250.png"]
