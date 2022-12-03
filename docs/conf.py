# -- Project information -----------------------------------------------------

project = "Sphinx Social Previews"
copyright = "2022, Executable Books Project"
author = "Executable Books Project"


# -- General configuration ---------------------------------------------------
extensions = ["sphinxext.opengraph", "sphinx_social_previews", "myst_parser"]
templates_path = []
source_suffix = ".rst"
main_doc = "index"
language = "en"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
pygments_style = "sphinx"


# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_book_theme"
# html_theme_options = {}
html_static_path = ["_static"]
html_logo = "_static/logo.png"
html_title = "Sphinx Social Previews"

ogp_site_url = "https://sphinx-social-previews.readthedocs.io/en/latest"
ogp_social_previews = {
    # "image_shadow": "_static/logo.png"
}
