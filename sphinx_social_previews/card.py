import hashlib
from pathlib import Path
import matplotlib
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from sphinxext.opengraph import get_tags
from sphinx.util import logging

matplotlib.use("agg")


LOGGER = logging.getLogger(__name__)
HERE = Path(__file__).parent
MAX_CHAR_PAGETITLE = 65
MAX_CHAR_DESCRIPTION = 155

DEFAULT_CONFIG = {
    "enable": True,
}


# These functions are used when creating social card objects to set MPL values.
# They must be defined here otherwise Sphinx errors when trying to pickle them.
# They are dependent on the `multiple` variable defined when the figure is created.
# Because they are depending on the figure size and renderer used to generate them.
def _set_pagetitle_line_width():
    return 850


def _set_description_line_width():
    return 1000


def setup_social_card_images(app):
    """Create matplotlib objects for saving social preview cards.

    This plots the final objects that are consistent across all pages.
    For example, site logo, shadow logo, line at the bottom.

    It plots placeholder text for text values because they change on each page.
    """
    config_social = DEFAULT_CONFIG.copy()
    config_social.update(app.config.ogp_social_previews)
    app.env.ogp_social_previews_config = config_social

    # If no social preview configuration, then just skip this
    if config_social.get("enable") is False:
        return

    LOGGER.info("Activated social media image previews...")
    kwargs = {}
    if config_social.get("image"):
        kwargs["image"] = Path(app.builder.srcdir) / config_social.get("image")
    elif app.config.html_logo:
        kwargs["image"] = Path(app.builder.srcdir) / app.config.html_logo

    # Grab the image shadow PNG for plotting
    if config_social.get("image_shadow"):
        kwargs["image_shadow"] = Path(app.builder.srcdir) / config_social.get(
            "image_shadow"
        )
    else:
        kwargs["image_shadow"] = Path(__file__).parent / "_static/logo-shadow.png"

    pass_through_config = ["text_color", "line_color", "background_color", "font"]
    for config in pass_through_config:
        if config_social.get(config):
            kwargs[config] = config_social.get(config)

    # Create the figure objects with placeholder text
    # Store in the Sphinx environment for re-use later
    fig, txt_site, txt_page, txt_description, txt_url = create_social_card_objects(
        **kwargs
    )
    app.env.social_card_plot_objects = [
        fig,
        txt_site,
        txt_page,
        txt_description,
        txt_url,
    ]


def create_social_card_objects(
    image=None,
    image_shadow=None,
    text_color="#4a4a4a",
    background_color="white",
    line_color="#5A626B",
    font="Roboto",
):
    # Load the Roboto font
    # TODO: Currently the `font` parameter above does nothing
    #   Should instead make it possible to load remote fonts or local fonts
    #   if a user specifies.
    path_font = Path(__file__).parent / "_static/Roboto-flex.ttf"
    font = matplotlib.font_manager.FontEntry(fname=str(path_font), name="Roboto")
    matplotlib.font_manager.fontManager.ttflist.append(font)

    # Because Matplotlib doesn't let you specify figures in pixels, only inches
    # This `multiple` results in a scale of about 1146px by 600px
    # Which is roughly the recommended size for OpenGraph images
    # ref: https://opengraph.xyz
    ratio = 1200 / 628
    multiple = 6
    fig = plt.figure(figsize=(ratio * multiple, multiple))
    fig.set_facecolor(background_color)

    # Text axis
    axtext = fig.add_axes((0, 0, 1, 1))

    # Image axis
    ax_x, ax_y, ax_w, ax_h = (0.69, 0.7, 0.25, 0.25)
    axim_logo = fig.add_axes((ax_x, ax_y, ax_w, ax_h), anchor="NE")

    # Image shadow axis
    ax_x, ax_y, ax_w, ax_h = (0.82, 0.1, 0.1, 0.1)
    axim_shadow = fig.add_axes((ax_x, ax_y, ax_w, ax_h), anchor="NE")

    # Line at the bottom axis
    axline = fig.add_axes((-0.1, -0.04, 1.2, 0.1))

    # Axes configuration
    left_margin = 0.05
    with plt.rc_context({"font.family": font.name, "text.color": text_color}):
        # Site title
        # Smaller font, just above page title
        site_title_y_offset = 0.9
        txt_site = axtext.text(
            left_margin,
            site_title_y_offset,
            "Test site title",
            {
                "size": 26,
            },
            ha="left",
            va="top",
            wrap=True,
        )

        # Page title
        # A larger font for more visibility
        page_title_y_offset = 0.8

        txt_page = axtext.text(
            left_margin,
            page_title_y_offset,
            "Test page title, a bit longer to demo",
            {"size": 42, "color": "k", "fontweight": "bold"},
            ha="left",
            va="top",
            wrap=True,
        )

        txt_page._get_wrap_line_width = _set_pagetitle_line_width

        # description
        # Just below site title, smallest font and many lines.
        # Our target length is 160 characters, so it should be
        # two lines at full width with some room to spare at this length.
        description_y_offset = 0.22
        txt_description = axtext.text(
            left_margin,
            description_y_offset,
            (
                "A longer description that we use to ,"
                "show off what the descriptions look like."
            ),
            {"size": 16},
            ha="left",
            va="bottom",
            wrap=True,
        )
        txt_description._get_wrap_line_width = _set_description_line_width

        # url
        # Aligned to the left of the shadow image
        url_y_axis_ofset = 0.12
        txt_url = axtext.text(
            left_margin,
            url_y_axis_ofset,
            "testurl.org",
            {"size": 22},
            ha="left",
            va="bottom",
            fontweight="bold",
        )

    if image_shadow:
        img = mpimg.imread(image_shadow)
        axim_shadow.imshow(img)

    # Put the logo in the top right if it exists
    if image:
        img = mpimg.imread(image)
        axim_logo.imshow(img)

    # Put a colored line at the bottom of the figure
    axline.hlines(0, 0, 1, lw=16, color=line_color)

    # Remove the ticks and borders from all axes for a clean look
    for ax in fig.axes:
        ax.set_axis_off()
    return fig, txt_site, txt_page, txt_description, txt_url


def render_page_card(app, pagename, templatename, context, doctree):
    """Create a social preview card using page metadata."""
    # If there's no document or if we haven't activated social cards, just skip
    if not doctree or not hasattr(app.env, "social_card_plot_objects"):
        return

    # This will exist if social_card_plot_objects exists
    config_social = app.env.ogp_social_previews_config

    # Grab the card creation objects from Sphinx environment
    # We just update them in order to save time
    (
        fig,
        txt_sitetitle,
        txt_pagetitle,
        txt_description,
        txt_url,
    ) = app.env.social_card_plot_objects

    # Tags contains the OGP metadata for this page
    tags = get_tags(app, context, doctree, app.config)

    def parse_ogp_tag(tags, entry):
        return (
            tags.split(entry)[-1].split("content=")[1].split("/>")[0].strip().strip('"')
        )

    # Description is the first few sentences of the page
    description = parse_ogp_tag(tags, "og:description")
    description_max_length = config_social.get(
        "description_max_length", MAX_CHAR_DESCRIPTION - 3
    )
    if len(description) > description_max_length:
        description = description[:description_max_length].strip() + "..."

    # Append the site URL to the description if requested
    # Description is the first few sentences of the page
    site_url = config_social.get("add_site_url", True)
    if site_url is True:
        url_text = app.config.ogp_site_url.split("://")[-1]
    elif isinstance(site_url, str):
        url_text = site_url

    # Page title is taken from the document
    pagetitle = parse_ogp_tag(tags, "og:title")
    if len(pagetitle) > MAX_CHAR_PAGETITLE:
        pagetitle = pagetitle[:MAX_CHAR_PAGETITLE] + "..."

    # Site title is taken from the Sphinx config
    sitetitle = context.get("docstitle", "")

    # Update the matplotlib text objects with new text from this page
    txt_sitetitle.set_text(sitetitle)
    txt_pagetitle.set_text(pagetitle)
    txt_description.set_text(description)
    txt_url.set_text(url_text)

    # Save the image to a static directory
    path_images = "_images/social_previews"
    static_dir = Path(app.builder.outdir) / path_images
    static_dir.mkdir(exist_ok=True, parents=True)
    path_out = f"summary_{pagename.replace('/', '_')}.png"

    # Save the figure
    fig.savefig(static_dir / path_out, facecolor=None)

    # Link the image in our page metadata
    url = app.config.ogp_site_url.strip("/")

    # Add a hash to the image based on metadata to bust caches
    # ref: https://developer.twitter.com/en/docs/twitter-for-websites/cards/guides/troubleshooting-cards#refreshing_images  # noqa
    hash = hashlib.sha1((sitetitle + pagetitle + description).encode()).hexdigest()
    path_out_image = f"{url}/{path_images}/{path_out}?{hash}"

    # Turn metatags into a list so we can easily add/remove
    metatags = context["metatags"].split("\n")

    # Find any og:image metadata tags and remove them
    # because we'll over-ride with this card
    og_image_lines = [ii for ii, tag in enumerate(metatags) if 'og:image"' in tag]
    for ii in og_image_lines[::-1]:
        metatags.pop(ii)

    # OpenGraph image tags
    metatags.append(f'<meta property="og:image" content="{path_out_image}" />')
    metatags.append('<meta property="og:image:width" content="1146" />')
    metatags.append('<meta property="og:image:height" content="600" />')

    # Twitter-specific tags
    metatags.append('<meta name="twitter:card" content="summary_large_image" />')

    # Overwrite metatags with our new version
    context["metatags"] = "\n".join(metatags)
