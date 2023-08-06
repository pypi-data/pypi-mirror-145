# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = "xotl.plato"
from datetime import datetime  # noqa

# Any year before to 2012 xotl.tools copyrights to "Medardo Rodriguez"
copyright = "2012-{} Merchise Autrement [~º/~] and Contributors"
copyright = copyright.format(datetime.now().year)
del datetime
author = "Merchise Autrement"

# The full version, including alpha/beta/rc tags
# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
try:
    from xotl.plato.release import VERSION
except ImportError:

    def up(path, level=1):
        result = path
        while level:
            result = os.path.dirname(result)
            level -= 1
        return result

    _current_dir = os.path.dirname(os.path.abspath(__file__))
    _project_dir = os.path.abspath(os.path.join(up(_current_dir, 2)))
    sys.path.append(_project_dir)
    from xotl.plato.release import VERSION

version = VERSION[: VERSION.rfind(".")]
release = VERSION


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
default_role = "code"
html_theme = "pyramid-roboto"
html_theme_path = [os.path.join("..", "theme")]

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ["_static"]


intersphinx_mapping = {
    "py": ("https://docs.python.org/3/", None),
    "xotless": ("https://merchise-autrement.gitlab.io/xotless/", None),
    "xotl.tools": ("https://merchise-autrement.gitlab.io/xotl.tools/", None),
    "gevent": ("http://www.gevent.org", None),
    "greenlet": ("https://greenlet.readthedocs.org/en/latest/", None),
    "hypothesis": ("https://hypothesis.readthedocs.io/en/latest/", None),
}

# Maintain the cache forever.
intersphinx_cache_limit = 365
