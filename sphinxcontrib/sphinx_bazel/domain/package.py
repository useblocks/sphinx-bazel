"""
bazel-package
=============
"""
from docutils import nodes
from docutils.parsers.rst import Directive, directives

from sphinx import addnodes
from sphinx.locale import _
from sphinx import addnodes

from sphinxcontrib.sphinx_bazel.domain.util import create_indexnode
from sphinxcontrib.sphinx_bazel.domain.object import BazelObject


class BazelPackage(BazelObject):
    """
    Directive to mark description of a new package.
    """

