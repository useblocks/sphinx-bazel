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
from sphinx.locale import l_
from sphinx.util.nodes import make_refnode

from sphinxcontrib.sphinx_bazel.domain.workspace import BazelWorkspace
from sphinxcontrib.sphinx_bazel.domain.object import BazelObject


class BazelDomain(Domain):
    """Bazel langage domain"""

    def merge_domaindata(self, docnames, otherdata):
        for fullname, (fn, objtype) in otherdata['objects'].items():
            if fn in docnames:
                self.data['objects'][fullname] = (fn, objtype)
        for modname, data in otherdata['modules'].items():
            if data[0] in docnames:
                self.data['modules'][modname] = data

    def resolve_any_xref(self, env, fromdocname, builder, target, node, contnode):
        workspace_name = node.get('bazel:workspace')
        package_name = node.get('py:class')
        results = []  # type: List[Tuple[str, nodes.Element]]
    
        # always search in "refspecific" mode with the :any: role
        matches = self.find_obj(env, workspace_name, package_name, target, None, 1)
        for name, obj in matches:
            if obj[1] == 'module':
                results.append(('py:mod',
                                self._make_module_refnode(builder, fromdocname,
                                                          name, contnode)))
            else:
                results.append(('py:' + self.role_for_objtype(obj[1]),
                                make_refnode(builder, fromdocname, obj[0], name,
                                             contnode, name)))

            return results

    name = 'bazel'
    label = 'Bazel'
    object_types = {
        'workspace': ObjType(l_('workspace'), 'workspace', 'ref'),
        'package': ObjType(l_('package'), 'package', 'ref'),
        'target': ObjType(l_('target'), 'target', 'ref'),
        'rule': ObjType(l_('rule'), 'rule', 'ref'),
        'macro': ObjType(l_('macro'), 'macro', 'ref'),
        'impl': ObjType(l_('impl'), 'impl', 'ref')
    }
    directives = {
        'workspace': BazelWorkspace,
        'package': BazelObject,
        'target': BazelObject,
        'rule': BazelObject,
        'macro': BazelObject,
        'implementation': BazelObject,
        'impl': BazelObject,
    }
    roles = {}
    initial_data = {
        'objects': {},
        'workspaces': {}
    }
    indices = []
    
    def clear_doc(self, docname):
        pass
