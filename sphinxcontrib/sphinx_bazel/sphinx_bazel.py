# -*- coding: utf-8 -*-

import sphinx
from pkg_resources import parse_version

from sphinxcontrib.sphinx_bazel.domain.domain import BazelDomain
from sphinxcontrib.sphinx_bazel.directives import AutobazelWorkspaceDirective


sphinx_version = sphinx.__version__
if parse_version(sphinx_version) >= parse_version("1.6"):
    from sphinx.util import logging
else:
    import logging

    logging.basicConfig()  # Only need to do this once

VERSION = '0.1.0'


def setup(app):
    log = logging.getLogger(__name__)
    app.add_domain(BazelDomain)
    app.add_directive('autobazel-workspace', AutobazelWorkspaceDirective)

    return {'version': VERSION}  # identifies the version of our extension

