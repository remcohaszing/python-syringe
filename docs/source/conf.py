# -*- encoding: utf-8 -*-

import pkg_resources

project = htmlhelp_basename = 'syringe'
pkg = pkg_resources.get_distribution(project)

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinxcontrib.napoleon'
]

intersphinx_mapping = {
    'python': ('http://docs.python.org/3.4', None)
}

source_suffix = '.rst'
master_doc = 'index'
copyright = '2014, Remco Haszing'
release = version = pkg.version
pygments_style = 'sphinx'
html_theme = 'default'
