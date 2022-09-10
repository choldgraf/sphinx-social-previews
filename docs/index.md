# Sphinx Social Cards

Automatically generate social media cards for your Sphinx documentation.

This extension will automatically generate a social media card with Matplotlib, using your site's title, logo, page title, and the first content from a given page.

To activate it, install and add it to your site's `conf.py` file:

```{code-block} python
:caption: conf.py

extensions = [
  ...,
  "sphinx-social-previews",
  ...
]
```
