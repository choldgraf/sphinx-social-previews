"""Add "social preview images" from page metadata."""

from .card import setup_social_card_images, render_page_card

__version__ = "0.0.1"


def setup(app):
    app.connect("builder-inited", setup_social_card_images)
    # Set priority slightly higher so it runs after the opengraph event
    app.connect("html-page-context", render_page_card, priority=501)
    app.add_config_value("ogp_social_previews", None, True)
