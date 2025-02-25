# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'PlasmidSeq Analysis Pipeline'
copyright = '2024, Rob Warden-Rothman'
author = 'Rob Warden-Rothman'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinxcontrib.mermaid',
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinx.ext.napoleon',
    'sphinx_tabs.tabs',
    'sphinx_copybutton',
]

source_suffix = ['.rst', '.md']

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = True
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

# Copybutton settings
copybutton_exclude = '.linenos, .gp, .go'

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

import sys
from pathlib import Path

sys.path.insert(0, str(Path('..', '..', 'AppContainer', 'app').resolve().absolute()))
# print(sys.path)


from sphinxcontrib import mermaid
MERMAID_INJECTION = """
var loader_info = {{name: 'logos', loader: () => fetch('https://unpkg.com/@iconify-json/logos@1/icons.json').then((res) => res.json())}}
mermaid.registerIconPacks([loader_info]);

"""

for cur_var in ['_MERMAID_RUN_NO_D3_ZOOM', '_MERMAID_RUN_D3_ZOOM']:
    blank_line, import_line, *remainder = getattr(mermaid, cur_var).splitlines(keepends=True)
    new_val = ''.join([blank_line, import_line, MERMAID_INJECTION, *remainder])
    # new_val = ''.join([blank_line, import_line, *remainder, MERMAID_INJECTION])
    print(new_val)
    setattr(mermaid, cur_var, new_val)