# User guide

This section covers how to install and use `sphinx-social-previews`.

## Install and enable the extension

First, install the extension:

```shell
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

## Add `sphinxext.opengraph` configuration

Add the `site_url` [configuration for sphinxext-opengraph](https://github.com/wpilibsuite/sphinxext-opengraph#options).
You may add other configuration for `sphinxext-opengraph` but this is the minimal information needed.

Build your documentation and you should now see image preview PNGs linked for each page.
They will be placed in `<build-folder>/_static/images/social_previews/`.

## Customize the card text

You can customize the card text by over-riding the OpenGraph metadata for each page.
See [the `sphinx-opengraph` documentation](https://github.com/wpilibsuite/sphinxext-opengraph) for more details.
