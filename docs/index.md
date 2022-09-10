# Sphinx Social Cards

Automatically generate social media cards for your Sphinx documentation.

This extension will automatically generate a social media card with Matplotlib, using your site's title, logo, page title, and the first content from a given page.

This package depends on [`sphinxext-opengraph`](https://github.com/wpilibsuite/sphinxext-opengraph), which allows you to embed OpenGraph metadata in your Sphinx website.

## Use

First, install the extension:

```
pip install git+https://github.com/choldgraf/sphinx-social-previews
```

Then activate this extension site's `conf.py` file:

```{code-block} python
:caption: conf.py

extensions = [
  ...,
  "sphinx-social-previews",
  ...
]
```

Finally, add the `site_url` [configuration for sphinxext-opengraph](https://github.com/wpilibsuite/sphinxext-opengraph#options).
You may add other configuration for `sphinxext-opengraph` but this is the minimal information needed.

Build your documentation and you should now see image preview PNGs linked for each page.
They will be placed in `<build-folder>/_static/images/social_previews/`.
