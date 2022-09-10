"""A small sphinx extension to add "copy" buttons to code blocks."""
from docutils.nodes import paragraph
from pathlib import Path
from matplotlib import pyplot as plt
import matplotlib.image as mpimg

__version__ = "0.1.0"

HERE = Path(__file__).parent
MAX_CHAR = 150

def render_page_card(app, pagename, templatename, context, doctree):
    """Create a social preview card using page metadata."""
    if not doctree:
        return

    # Set up metadata for the card
    sitetitle = context.get("docstitle", "")
    pagetitle = context.get("title", "")
    image = context.get("logo", "")
    if image:
        image = Path(app.builder.srcdir) / "_static" / image
    
    tagline = " ".join([ii.astext() for ii in doctree.traverse(paragraph)])
    tagline = tagline.replace("\n\n", "\n")
    tagline = tagline.replace("\n", "")
    if len(tagline) > MAX_CHAR:
        tagline = tagline[:MAX_CHAR].rsplit(" ", 1)[0] + "..."

    # Generate the card
    fig = create_social_card(sitetitle, pagetitle, tagline, image)
    
    # Save the image to a static directory
    static_dir = Path(app.builder.outdir) / "_static/images/social_previews"
    static_dir.mkdir(exist_ok=True, parents=True)
    path_out = f"summary_{pagename.replace('/', '_')}.png"
    fig.savefig(static_dir / path_out)
    
    # Link the image in our page metadata
    url = app.config.ogp_site_url.strip("/")
    path_out_image = f"{url}/_static/images/social_previews/{path_out}"
    context[
        "metatags"
    ] += f'<meta property="og:image" content="{path_out_image}" />'
    context[
        "metatags"
    ] += f'<meta name="twitter:card" content="summary_large_image" />'


def create_social_card(site_title, page_title, tagline, image=None, text_color="#7e7e7e", background_color="white", font="Roboto"):
    # Size of figure
    ratio = 800 / 418
    multiple = 3
    fig = plt.figure(figsize=(ratio * multiple, multiple))
    fig.set_facecolor(background_color)
    left_margin = 0.06

    with plt.rc_context({"font.sans-serif": [font], "text.color": text_color}):
        axtext = fig.add_axes((0, 0, 1, 1))
        txt_title = axtext.text(
            left_margin,
            0.86,
            site_title,
            {
                "size": 16,
            },
            ha="left",
            va="top",
            wrap=True,
        )
        txt_page = axtext.text(
            left_margin,
            0.7,
            page_title,
            {"size": 22, "fontweight": "bold"},
            ha="left",
            va="top",
            wrap=True,
        )
        txt_page._get_wrap_line_width = lambda: 450

        txt_tagline = axtext.text(
            left_margin, 0.1, tagline, {"size": 11}, ha="left", va="bottom", wrap=True
        )
        txt_tagline._get_wrap_line_width = lambda: 450
        
        # Turn off the axis so we see no ticks
        axtext.set_axis_off()

    # Put the logo in the top right if it exists
    if image:
        img = mpimg.imread(image)
        axim = fig.add_axes((0.70, 0.70, 0.25, 0.25), anchor="NE")
        axim.imshow(img)
        axim.set_axis_off()
    return fig


def setup(app):
    app.connect("html-page-context", render_page_card)
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
