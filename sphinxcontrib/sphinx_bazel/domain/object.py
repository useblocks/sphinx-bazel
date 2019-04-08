import re

from docutils.parsers.rst import directives, nodes

from pkg_resources import parse_version

import sphinx
from sphinx import addnodes
from sphinx.directives import ObjectDescription


sphinx_version = sphinx.__version__
if parse_version(sphinx_version) >= parse_version("1.6"):
    from sphinx.util import logging
else:
    import logging
logger = logging.getLogger(__name__)

# REs for Bazel signatures
bzl_sig_re = re.compile(
    r'''^  \/\/([\w\/]*)     # package name
           (:([\w\/.-]*))?   # target name
           (:([\w\/.-]*))?   # rule, macro or impl name (named later internally as internal)
           (:([\w\/.-]*))?   # attribute name 
           $                 # and nothing more
          ''', re.VERBOSE)


class BazelObject(ObjectDescription):
    """
    Description of a general bazel object
    """
    option_spec = {
        'path': directives.unchanged,  # Can be used to specify local, not-valid workspace
        'implementation': directives.unchanged,  # Used by bazel:rule to define implementation function
        'invocation': directives.unchanged,  # Used to define a string which represents a complete call
        'show_workspace': directives.flag,
        'show_workspace_path': directives.flag,
        'show_implementation': directives.flag,
        'show_invocation': directives.flag,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.implementation = None
        self.invocation = None
        self.specific_workspace_path = None

    def get_signature_prefix(self, sig):
        # type: (str) -> str
        """May return a prefix to put before the object name in the
        signature.
        """
        return ''

    def needs_arglist(self):
        # type: () -> bool
        """May return true if an empty argument list is to be generated even if
        the document contains none.
        """
        return False

    def handle_signature(self, sig, signode):
        """
        Transform a Bazel signatur into RST nodes.

        :param sig:
                :param signode:
        :return:
        """
        m = bzl_sig_re.match(sig)
        if m is None:
            logger.error("Sphinx-Bazel: Parse problems with signature: {}".format(sig))
            raise ValueError
        package, after_package, target, after_target, internal, after_internal, attribute = m.groups()

        # Let's see if we have to use a specific workspace path or if we have to use the latest defined workspace
        self.specific_workspace_path = self.options.get('path', None)
        if self.specific_workspace_path:
            signode['workspace'] = self.specific_workspace_path
        else:
            try:
                signode['workspace'] = self.env.ref_context['bazel:workspace']
            except KeyError:
                logger.error("No workspace defined before given {} on page {} line {}".format(
                    self.name, self.state.document.current_source, self.state.document.current_line))

        signode['package'] = package
        signode['target'] = target

        sig_text = '//{}'.format(package)
        if target:
            sig_text += ':{}'.format(target)
        if internal:
            sig_text += ':{}'.format(internal)
        if attribute:
            sig_text += ':{}'.format(attribute)
        signode += addnodes.desc_name(sig_text, sig_text)

        if self.options.get('show_workspace', False) is None:  # if flag is set, value is None
            ws_string = 'workspace: {}'.format(signode['workspace'])
            self._add_signature_detail(signode, ws_string)

        if self.options.get('show_workspace_path', False) is None:  # if flag is set, value is None
            # If no extra workspace path was defined via :path:
            if self.specific_workspace_path is None:
                # Get the path of the current/latest workspace
                current_ws = self.env.ref_context['bazel:workspace']
                ws_obj = self.env.domaindata['bazel']['workspaces'][current_ws]
                ws_path = ws_obj[1]  # See workspace.py for details about stored data
            else:
                ws_path = self.specific_workspace_path
            ws_path_string = 'workspace path: {}'.format(ws_path)
            self._add_signature_detail(signode, ws_path_string)

        rule_impl = self.options.get('implementation', "")
        if rule_impl:
            self.implementation = rule_impl

        rule_invocation = self.options.get('invocation', "")
        if rule_invocation:
            self.invocation = rule_invocation

        if self.options.get('show_implementation', False) is None:
            impl_string = 'implementation: {}'.format(self.implementation)
            self._add_signature_detail(signode, impl_string)

        if self.options.get('show_invocation', False) is None:
            invocation_string = 'invocation: {}'.format(self.invocation)
            self._add_signature_detail(signode, invocation_string)

        return sig, sig

    def _add_signature_detail(self, signode, text):
        """
        Create a additional line under signature.
        Used to show additional details of an object like workspace name or path

        :param signode: node to add the line add the ending
        :param text: Text inside the new line
        :return: None
        """
        ws_line = nodes.line()
        ws_line += addnodes.desc_addname(text, text)
        signode += ws_line

