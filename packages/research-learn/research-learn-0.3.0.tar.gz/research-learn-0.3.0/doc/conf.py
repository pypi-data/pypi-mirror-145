import sys
import os

import sphinx_rtd_theme

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'numpydoc',
]
numpydoc_show_class_members = False
import sphinx
from distutils.version import LooseVersion
if LooseVersion(sphinx.__version__) < LooseVersion('1.4'):
    extensions.append('sphinx.ext.pngmath')
else:
    extensions.append('sphinx.ext.imgmath')
autodoc_default_flags = ['members', 'inherited-members']
templates_path = ['_templates']
autosummary_generate = True
source_suffix = '.rst'
plot_gallery = 'True'
master_doc = 'index'

# General information about the project.
project = u'research-learn'
copyright = u'2019, Georgios Douzas'
from rlearn import __version__
version = __version__
release = __version__
exclude_patterns = ['_build', '_templates']
pygments_style = 'sphinx'
html_style = 'css/research-learn.css'
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_static_path = ['_static']
htmlhelp_basename = 'research-learndoc'
latex_documents = [
  ('index', 'research-learn.tex', u'research-learn Documentation',
   u'Georgios Douzas', 'manual'),
]
man_pages = [
    ('index', 'research-learn.tex', u'research-learn Documentation',
     [u'Georgios Douzas'], 1)
]
texinfo_documents = [
  ('index', 'research-learn', u'research-learn Documentation',
   u'Georgios Douzas', 'research-learn', 'Toolbox for reproducible research in machine learning.',
   'Miscellaneous'),
]
intersphinx_mapping = {
    'python': ('https://docs.python.org/{.major}'.format(
        sys.version_info), None),
    'numpy': ('https://docs.scipy.org/doc/numpy/', None),
    'scipy': ('https://docs.scipy.org/doc/scipy/reference', None),
    'matplotlib': ('https://matplotlib.org/', None),
    'sklearn': ('http://scikit-learn.org/stable', None),
    'somoclu': ('https://somoclu.readthedocs.io/en/stable', None)
}
sphinx_gallery_conf = {
    'doc_module': 'rlearn',
    'backreferences_dir': os.path.join('generated'),
    'reference_url': {
        'rlearn': None}
}

def setup(app):
    # a copy button to copy snippet of code from the documentation
    app.add_js_file('js/copybutton.js')
