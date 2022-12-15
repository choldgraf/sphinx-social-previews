"""
A helper script to test out what social previews look like.
I should remove this when I'm happy with the result.
"""
# %load_ext autoreload
# %autoreload 2

from sphinx_social_previews.card import create_social_card_objects
from pathlib import Path

tagline = "This is a tagline, it's a little longer than the rest. " * 5
fig, txtsite, txtpage, txtdesc, txturl = create_social_card_objects(
    image="docs/_static/logo.png",
    image_shadow="sphinx_social_previews/_static/logo-shadow.png",
)

# These are roughly the max characters we enforce
# Leaving here for texting
MAX_CHAR_PAGETITLE = 70
MAX_CHAR_DESCRIPTION = 160

for length in [1, 3, 5, 7, 9]:
    txtsite.set_text("Chris Holdgraf's website")
    n_words = MAX_CHAR_PAGETITLE // length
    title = (("A" * length + " ") * n_words) + "..."
    txtpage.set_text(title)
    desc = (("B" * length + " ") * n_words * 2) + "..."
    txtdesc.set_text(desc)
    txturl.set_text("chrisholdgraf.com")
    Path("tmp").mkdir(exist_ok=True)
    fig.savefig(f"./tmp/{length}.png", facecolor="w")
