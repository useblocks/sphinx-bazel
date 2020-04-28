"""
Bazel domain implementation for Sphinx.

Domain overview
===============

* **workspace**: contains the ``WORKSPACE`` file. Container for multiple packages

 * **package**: contains a ``BUILD`` file. Container for multiple targets

  * **target**: any file or .bzl-file. If last, following is available:

   * **rule**:  a defined rule inside a .bzl-file
   * **macro**: a defined macro-function inside a .bzl file


Domain directives
=================

* bazel-workspace
* bazel-package
* bazel-target
* bazel-rule
* bazel-macro
"""

# Implementation details/help taken from:
# Domains user manual : http://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html
# Domains API: http://www.sphinx-doc.org/en/master/extdev/domainapi.html#domain-api
# Python Domain impl: https://github.com/sphinx-doc/sphinx/blob/master/sphinx/domains/python.py
# Java Domain impl: https://github.com/bronto/javasphinx/tree/master/javasphinx

from sphinx.domains import Domain, ObjType
from sphinx.locale import _

from sphinxcontrib.sphinx_bazel.domain.workspace import BazelWorkspace
from sphinxcontrib.sphinx_bazel.domain.object import BazelObject


class BazelDomain(Domain):
    """Bazel langage domain"""

    name = 'bazel'
    label = 'Bazel'
    object_types = {
        'workspace': ObjType(_('workspace'), 'workspace', 'ref'),
        'package': ObjType(_('package'), 'package', 'ref'),
        'target': ObjType(_('target'), 'target', 'ref'),
        'rule': ObjType(_('rule'), 'rule', 'ref'),
        'macro': ObjType(_('macro'), 'macro', 'ref'),
        'impl': ObjType(_('impl'), 'impl', 'ref'),
        'attribute': ObjType(_('attribute'), 'attribute', 'ref')
    }
    directives = {
        'workspace': BazelWorkspace,
        'package': BazelObject,
        'target': BazelObject,
        'rule': BazelObject,
        'macro': BazelObject,
        'implementation': BazelObject,
        'impl': BazelObject,
        'attribute': BazelObject,
    }
    roles = {}
    initial_data = {
        'objects': {},
        'workspaces': {}
    }
    indices = []

    def clear_doc(self, docname):
        pass
