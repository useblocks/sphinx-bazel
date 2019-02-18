# -*- coding: utf-8 -*-

import os
import random
import string

import sphinx
from sphinx.errors import SphinxError
from docutils import nodes
from docutils.parsers.rst import directives
from pkg_resources import parse_version
from sphinx.roles import XRefRole

sphinx_version = sphinx.__version__
if parse_version(sphinx_version) >= parse_version("1.6"):
    from sphinx.util import logging
else:
    import logging

    logging.basicConfig()  # Only need to do this once

VERSION = '0.1.0'


def setup(app):
    log = logging.getLogger(__name__)
    app.add_config_value('needs_template', "default value", 'html')

    # Define nodes
    # app.add_node(Need, html=(html_visit, html_depart), latex=(latex_visit, latex_depart))
    
    # app.add_directive('needimport', NeedimportDirective)

    ########################################################################
    # ROLES
    ########################################################################
    # # Provides :need:`ABC_123` for inline links.
    # app.add_role('need', XRefRole(nodeclass=Need_ref,
    #                               innernodeclass=nodes.emphasis,
    #                               warn_dangling=True))
    
    ########################################################################
    # EVENTS
    ########################################################################
    # Make connections to events
    # app.connect('doctree-resolved', add_sections)

    return {'version': VERSION}  # identifies the version of our extension


def visitor_dummy(*args, **kwargs):
    """
    Dummy class for visitor methods, which does nothing.
    """
    pass


def prepare_env(app, env, docname):
    """
    Prepares the sphinx environment to store sphinx-needs internal data.
    """
    if not hasattr(env, 'needs_all_needs'):
        # Used to store all needed information about all needs in document
        env.needs_all_needs = {}

    if not hasattr(env, 'needs_functions'):
        # Used to store all registered functions for supporting dynamic need values.
        env.needs_functions = {}
        needs_functions = getattr(app.config, 'needs_functions', [])
        if needs_functions is None:
            needs_functions = []
        if not isinstance(needs_functions, list):
            raise SphinxError('Config parameter needs_functions must be a list!')

        # Register built-in functions
        for need_common_func in needs_common_functions:
            register_func(env, need_common_func)

        # Register functions configured by user
        for needs_func in needs_functions:
            register_func(app, needs_func)

    app.config.needs_hide_options += ['hidden']
    app.config.needs_extra_options['hidden'] = directives.unchanged

    if not hasattr(env, 'needs_workflow'):
        # Used to store workflow status information for already executed tasks.
        # Some tasks like backlink_creation need be be performed only once.
        # But most sphinx-events get called several times (for each single document file), which would also
        # execute our code several times...
        env.needs_workflow = {
            'backlink_creation': False,
            'dynamic_values_resolved': False
        }
