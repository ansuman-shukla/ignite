# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/stable/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath("../.."))
import ignite
import pytorch_sphinx_theme

# -- Project information -----------------------------------------------------

project = "ignite"
copyright = "2020, PyTorch-Ignite Contributors"
author = "PyTorch-Ignite Contributors"

# The short X.Y version
try:
    version = os.environ["code_version"]
    if "master" in version:
        version = "master (" + ignite.__version__ + ")"
    else:
        version = version.replace("v", "")
except KeyError:
    version = ignite.__version__

# The full version, including alpha/beta/rc tags
release = "master"


# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosectionlabel",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path .
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "pytorch_sphinx_theme"
html_theme_path = [pytorch_sphinx_theme.get_html_theme_path()]

html_theme_options = {
    "canonical_url": "https://pytorch.org/ignite/index.html",
    "collapse_navigation": False,
    "display_version": True,
    "logo_only": True,
}

html_logo = "_static/img/ignite_logo.svg"

html_favicon = "_templates/_static/img/ignite_logomark.svg"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static", "_templates/_static"]

html_context = {
    "css_files": [
        # 'https://fonts.googleapis.com/css?family=Lato',
        # '_static/css/pytorch_theme.css'
        "_static/css/ignite_theme.css"
    ],
}


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "ignitedoc"


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',
    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, "ignite.tex", "ignite Documentation", "Torch Contributors", "manual"),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, "ignite", "ignite Documentation", [author], 1)]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "ignite",
        "ignite Documentation",
        author,
        "ignite",
        "One line description of project.",
        "Miscellaneous",
    ),
]


# -- Extension configuration -------------------------------------------------

# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {"https://docs.python.org/": None}

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# -- Type hints configs ------------------------------------------------------

autodoc_typehints = "signature"

# -- A patch that turns-off cross refs for type annotations ------------------

import sphinx.domains.python
from docutils import nodes
from sphinx import addnodes

# replaces pending_xref node with desc_type for type annotations
sphinx.domains.python.type_to_xref = lambda t, e=None: addnodes.desc_type("", nodes.Text(t))

# -- Autosummary patch to get list of a classes, funcs automatically ----------

from importlib import import_module
from inspect import getmembers, isclass, isfunction
import sphinx.ext.autosummary
from sphinx.ext.autosummary import Autosummary
from docutils.parsers.rst import directives
from docutils.statemachine import StringList


class BetterAutosummary(Autosummary):
    """Autosummary with autolisting for modules.

    By default it tries to import all public names (__all__),
    otherwise import all classes and/or functions in a module.

    Options:
    - :autolist: option to get list of classes and functions from currentmodule.
    - :autolist-classes: option to get list of classes from currentmodule.
    - :autolist-functions: option to get list of functions from currentmodule.

    Example Usage:

    .. currentmodule:: ignite.metrics

    .. autosummary::
        :nosignatures:
        :autolist:
    """

    # Add new option
    _option_spec = Autosummary.option_spec.copy()
    _option_spec.update(
        {
            "autolist": directives.unchanged,
            "autolist-classes": directives.unchanged,
            "autolist-functions": directives.unchanged,
        }
    )
    option_spec = _option_spec

    def run(self):
        for auto in ("autolist", "autolist-classes", "autolist-functions"):
            if auto in self.options:
                # Get current module name
                module_name = self.env.ref_context.get("py:module")
                # Import module
                module = import_module(module_name)

                # Get public names (if possible)
                try:
                    names = getattr(module, "__all__")
                except AttributeError:
                    # Get classes defined in the module
                    cls_names = [
                        name[0]
                        for name in getmembers(module, isclass)
                        if name[-1].__module__ == module_name and not (name[0].startswith("_"))
                    ]
                    # Get functions defined in the module
                    fn_names = [
                        name[0]
                        for name in getmembers(module, isfunction)
                        if (name[-1].__module__ == module_name) and not (name[0].startswith("_"))
                    ]
                    names = cls_names + fn_names
                    # It may happen that module doesn't have any defined class or func
                    if not names:
                        names = [name[0] for name in getmembers(module)]

                # Filter out members w/o doc strings
                names = [name for name in names if getattr(module, name).__doc__ is not None]

                if auto == "autolist":
                    # Get list of all classes and functions inside module
                    names = [
                        name for name in names if (isclass(getattr(module, name)) or isfunction(getattr(module, name)))
                    ]
                else:
                    if auto == "autolist-classes":
                        # Get only classes
                        check = isclass
                    elif auto == "autolist-functions":
                        # Get only functions
                        check = isfunction
                    else:
                        raise NotImplementedError

                    names = [name for name in names if check(getattr(module, name))]

                # Update content
                self.content = StringList(names)
        return super().run()


# Patch original Autosummary
sphinx.ext.autosummary.Autosummary = BetterAutosummary
