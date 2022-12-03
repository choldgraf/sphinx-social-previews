"""Add "social preview images" from page metadata."""

from .card import setup_social_card_images, render_page_card

__version__ = "0.0.1"


def setup(app):
    app.connect("builder-inited", setup_social_card_images)
    app.connect("html-page-context", render_page_card)
    app.add_config_value("ogp_social_previews", None, True)
