from subprocess import run
from pathlib import Path

# -- Project information -----------------------------------------------------

project = "Sphinx Social Previews"
copyright = "2022, Executable Books Project"
author = "Executable Books Project"


# -- General configuration ---------------------------------------------------
extensions = ["sphinx_social_previews", "myst_parser", "sphinx_design"]
templates_path = []
source_suffix = ".rst"
main_doc = "index"
language = "en"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "tmp"]
pygments_style = "sphinx"


# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_book_theme"
# html_theme_options = {}
html_static_path = ["_static"]
html_logo = "_static/logo.png"
html_title = "Sphinx Social Previews"

ogp_site_url = "https://sphinx-social-previews.readthedocs.io/en/latest"
ogp_social_previews = {
    # "image_mini": "_static/logo.png",
}

# Generate example images for documentation
here = Path(__file__).parent
run(f"python {here / 'script/test_previews.py'}", shell=True)
