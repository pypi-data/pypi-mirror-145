import os
import sys

html_theme = 'sphinx_rtd_theme'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.linkcode',
]

def linkcode_resolve(domain, info):
    if domain != 'py':
        return None
    if not info['module']:
        return None
    filename = info['module'].replace('.', '/')
    link = f"https://github.com/sustglobal/dev-center/tree/master/clients/python/{filename}.py"
    return link

# force documentation of __init__ as separate entities to we can hide
# constructors for classes that should never be instantiated by users.
autodoc_class_signature = "separated"
